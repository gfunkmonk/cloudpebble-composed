/*
 * Copyright 2014 Fitbit, Inc.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *   1. Redistributions of source code must retain the above copyright notice,
 *      this list of conditions and the following disclaimer.
 *   2. Redistributions in binary form must reproduce the above copyright
 *      notice, this list of conditions and the following disclaimer in the
 *      documentation and/or other materials provided with the distribution.
 *   3. Neither the name of the copyright holder nor the names of its
 *      contributors may be used to endorse or promote products derived from
 *      this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

var WebSocket = require('ws');
var server = require('../server');
var connection = require('../connection');
var connectionManager = require('../connection-manager');
var TestClientManager = require('./test-client').TestClientManager;
var assert = require('assert');
var testUtils = require('./test-utils');
var testAuthServer = require('./test-auth-server');
var config = require('../config');

var MessageType = connection.MessageType;
var CloseCode = connection.CloseCode;

require('co-mocha');

describe('cloudpebble websocket proxy', function () {
  var toolUrl;
  var deviceUrl;
  var toolClient;
  var deviceClient;
  var m;

  var testClientManager = new TestClientManager();

  function* createTestClient (url) {
    return yield testClientManager.createTestClient(url);
  }

  before(function (done) {
    config.pebbleAuthUrl = testAuthServer.getServerURL();
    done();
  });

  beforeEach(function (done) {
    // Start a new server each time
    // TODO reset ConnectionManager
    server.listen(0, function () {
      toolUrl = "ws://localhost:" + server.address().port + "/tool";
      deviceUrl = "ws://localhost:" + server.address().port + "/device";
      done();
    });
  });

  afterEach(function (done) {
    toolClient = null;
    deviceClient = null;

    testClientManager.closeAll();
    testUtils.cleanupServer(server, function () {
      done();
    });
  });

  describe('tool client', function () {
    beforeEach(function* () {
      toolClient = yield createTestClient(toolUrl);
    });

    it('can authenticate with the proxy', function* () {
      yield toolClient.authorize('xxx');
    });

    it('receives an auth failure error if the access token is invalid', function* () {
      yield toolClient.failToAuthorize('xxx-invalid');
    });

    it('is disconnected with an error for non-binary data', function* () {
      toolClient.send("hello world");
      var closeCode = yield toolClient.waitForClose();
      assert.equal(closeCode, CloseCode.UnsupportedDataType);
    });

    it('ignores messages if not authenticated yet', function* () {
      toolClient.send(new Buffer([0x1234]));

      // TODO: verify that messages were ignored?
    });

    it('ignores messages if there is no peer connected', function* () {
      yield toolClient.authorize('xxx');
      toolClient.send(new Buffer([0x1234]));

      // TODO: verify that messages were ignored?
    });

    it('responds with an auth error if auth server is down', function* () {
      var oldUrl = config.pebbleAuthUrl;
      try {
        config.pebbleAuthUrl = "http://localhost:1/";

        yield toolClient.failToAuthorize('xxx');
      } finally {
        config.pebbleAuthUrl = oldUrl;
      }
    });

    it('responds with an auth error if the token does not have a user id', function* () {
        yield toolClient.failToAuthorize('userless-token');
    });

    it('handles client disconnect while authorization is pending', function* () {
      try {
        testAuthServer.setBeforeAuth(function* () {
          toolClient.close();
        });

        toolClient.sendAccessToken('xxx');

        yield testUtils.waitForEvent(connectionManager, 'connection:remove');

        // make sure connection was removed
        assert.equal(connectionManager.getNumberOfAuthorizedConnections(), 0);
        assert.equal(connectionManager.getNumberOfConnections(), 0);
      } finally {
        testAuthServer.setBeforeAuth(null);
      }
    });
  });

  it('limits the number of device connections per account', function* () {
    var deviceClients = [];
    try {
      for (var i = 0; i < config.maxDevicesPerAccount + 5; i += 1) {
        var client = yield createTestClient(deviceUrl);
        deviceClients.push(client);
        yield client.authorize('auth1b');

        var numAuthorized = connectionManager.getNumberOfAuthorizedConnections();
        assert.ok(numAuthorized <= config.maxDevicesPerAccount, 'too many device connections');
      }
    } finally {
      deviceClients.forEach(function (c) {
        c.close();
      });
    }
  });

  function commonTests () {
    it('both connections are notified that the other side is connected', function* () {
      // if we got this far, we're good
    });

    it('can send messages from the tool to the device', function* () {
      var pingMessage = new Buffer([
        MessageType.WatchToPhone, 0x07, 0xd1, 0x06, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00
      ]);

      toolClient.send(pingMessage);
      var deviceMessage = yield deviceClient.nextMessage();
      assert.deepEqual(pingMessage, deviceMessage);
    });

    it('can send messages from the device to the tool', function* () {
      var pongMessage = new Buffer([
        MessageType.PhoneToWatch, 0x07, 0xd1, 0x06, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00
      ]);

      deviceClient.send(pongMessage);
      var toolMessage = yield toolClient.nextMessage();
      assert.deepEqual(pongMessage, toolMessage);
    });

    it('disconnects the tool client if a second tool connects to the same account', function* () {
      var toolClient2 = yield createTestClient(toolUrl);
      yield toolClient2.authorize('auth1a');

      try {
        var closeCode = yield toolClient.waitForClose();
        assert.equal(closeCode, CloseCode.ConnectionReplaced);
      } finally {
        toolClient2.close();
      }
    });

    describe('when a new device connects', function () {
      var deviceClient2;

      beforeEach(function* () {
        deviceClient2 = yield createTestClient(deviceUrl);
        yield deviceClient2.authorize('auth1b');

        // Tool should get a disconnected and connected message
        var toolMessage = yield toolClient.nextMessage();
        assert.equal(toolMessage[0], MessageType.ProxyConnectionStatusUpdate);
        assert.equal(toolMessage[1], 0x00);

        toolMessage = yield toolClient.nextMessage();
        assert.equal(toolMessage[0], MessageType.ProxyConnectionStatusUpdate);
        assert.equal(toolMessage[1], 0xFF);

        // Old device connection should get a disconnected message
        var deviceMessage = yield deviceClient.nextMessage();
        assert.equal(deviceMessage[0], MessageType.ProxyConnectionStatusUpdate);
        assert.equal(deviceMessage[1], 0x00);

        // New device connection should get a connected message
        var deviceMessage2 = yield deviceClient2.nextMessage();
        assert.equal(deviceMessage[0], MessageType.ProxyConnectionStatusUpdate);
        assert.equal(deviceMessage2[1], 0xFF);
      });

      afterEach(function* () {
        deviceClient2.close();
      });

      it('clients get disconnected/connected messages', function* () {
        // everything is handled in the beforeEach function
      });

      it('messages are routed to the new device', function* () {
        var pingMessage = new Buffer([
          MessageType.WatchToPhone, 0x07, 0xd1, 0x06, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00
        ]);

        toolClient.send(pingMessage);

        var deviceMessage2 = yield deviceClient2.nextMessage();
        assert.deepEqual(pingMessage, deviceMessage2);

        deviceClient2.close();
      });
    });
  }

  describe('tool client connects first, device client connects second', function () {
    beforeEach(function* () {
      toolClient = yield createTestClient(toolUrl);
      yield toolClient.authorize('auth1a');

      deviceClient = yield createTestClient(deviceUrl);
      yield deviceClient.authorize('auth1b');

      var toolMessage = yield toolClient.nextMessage();
      assert.equal(toolMessage[0], MessageType.ProxyConnectionStatusUpdate);
      assert.equal(toolMessage[1], 0xFF);

      var deviceMessage = yield deviceClient.nextMessage();
      assert.equal(deviceMessage[0], MessageType.ProxyConnectionStatusUpdate);
      assert.equal(deviceMessage[1], 0xFF);
    });

    commonTests();
  });

  describe('device client connects first, tool client connects second', function () {
    beforeEach(function* () {
      deviceClient = yield createTestClient(deviceUrl);
      yield deviceClient.authorize('auth1b');

      toolClient = yield createTestClient(toolUrl);
      yield toolClient.authorize('auth1a');

      var deviceMessage = yield deviceClient.nextMessage();
      assert.equal(deviceMessage[0], MessageType.ProxyConnectionStatusUpdate);
      assert.equal(deviceMessage[1], 0xFF);

      var toolMessage = yield toolClient.nextMessage();
      assert.equal(toolMessage[0], MessageType.ProxyConnectionStatusUpdate);
      assert.equal(toolMessage[1], 0xFF);
    });

    commonTests();
  });
});
