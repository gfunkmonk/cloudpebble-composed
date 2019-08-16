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

var Connection = require('../connection').Connection;
var connectionManager = require('../connection-manager');
var WebSocket = require('ws');
var server = require('../server');
var assert = require('assert');
var TestClientManager = require('./test-client').TestClientManager;
var testAuthServer = require('./test-auth-server');
var testUtils = require('./test-utils');
var config = require('../config');

describe('connectionManager', function () {
  var toolUrl;
  var deviceUrl;

  var testClientManager = new TestClientManager();

  function* createTestClient (url) {
    return yield testClientManager.createTestClient(url);
  }

  before(function* () {
    var testServerConfig = yield testUtils.setupTestServer();
    toolUrl = testServerConfig.toolUrl;
    deviceUrl = testServerConfig.deviceUrl;
  });

  after(function (done) {
    testClientManager.closeAll();
    testUtils.cleanupServer(server, done);
  });

  describe('#registerConnection', function () {
    it('throws an exception if connection argument is not provided', function (done) {
      assert.throws(function () {
        connectionManager.registerConnection(null);
      }, Error);
      done();
    });

    it('throws an exception if connection is not authenticated', function* () {
      var toolClient = yield createTestClient(toolUrl);

      try {
        var conn = connectionManager.getAllConnections()[0];

        assert.throws(function () {
          connectionManager.registerConnection(conn);
        }, Error);
      } finally {
        toolClient.close();
      }
    });
  });

  describe('#getNumberOfConnections', function () {
    it('the number of connections changes when clients connect and disconnect', function* () {
      assert.equal(connectionManager.getNumberOfConnections(), 0);
      assert.equal(connectionManager.getNumberOfAuthorizedConnections(), 0);

      var toolClient = yield createTestClient(toolUrl);
      var deviceClient = yield createTestClient(deviceUrl);
      var deviceClient2 = yield createTestClient(deviceUrl);

      try {
        assert.equal(connectionManager.getNumberOfConnections(), 3);

        yield toolClient.authorize('xxx');
        assert.equal(connectionManager.getNumberOfAuthorizedConnections(), 1);

        yield deviceClient.authorize('xxx');
        assert.equal(connectionManager.getNumberOfAuthorizedConnections(), 2);

        yield deviceClient2.authorize('xxx');
        assert.equal(connectionManager.getNumberOfAuthorizedConnections(), 3);

        toolClient.close();
        yield testUtils.waitForEvent(connectionManager, 'connection:remove');
        assert.equal(connectionManager.getNumberOfAuthorizedConnections(), 2);

        deviceClient.close();
        yield testUtils.waitForEvent(connectionManager, 'connection:remove');
        assert.equal(connectionManager.getNumberOfAuthorizedConnections(), 1);

        deviceClient2.close();
        yield testUtils.waitForEvent(connectionManager, 'connection:remove');
        assert.equal(connectionManager.getNumberOfAuthorizedConnections(), 0);

      } finally {
        toolClient.close();
        deviceClient.close();
        deviceClient2.close();
      }

      assert.equal(connectionManager.getNumberOfConnections(), 0);
    });
  });
});
