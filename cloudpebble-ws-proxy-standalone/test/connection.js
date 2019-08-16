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

var testUtils = require('./test-utils');
var TestClientManager = require('./test-client').TestClientManager;
var server = require('../server');
var connectionManager = require('../connection-manager');
var sinon = require('sinon');
var WebSocket = require('ws');
var config = require('../config');
var assert = require('assert');
var connection = require('../connection');

var CloseCode = connection.CloseCode;

describe('connection', function () {
  var toolUrl;
  var toolClient;
  var sandbox;
  var conn;

  var testClientManager = new TestClientManager();

  function* createTestClient (url) {
    return yield testClientManager.createTestClient(url);
  }

  beforeEach(function* () {
    sandbox = sinon.sandbox.create();

    var testServerConfig = yield testUtils.setupTestServer();
    toolUrl = testServerConfig.toolUrl;

    toolClient = yield createTestClient(toolUrl);

    assert.equal(connectionManager.getNumberOfConnections(), 1);
    conn = connectionManager.getAllConnections()[0];
  });

  afterEach(function (done) {
    toolClient.close();
    testClientManager.closeAll();

    // Note that this could time out if there's any sockets still open
    testUtils.cleanupServer(server, function () {
      sandbox.restore();
      done();
    });
  });

  it('ignores closing if already closed', function* () {
    conn.close();
    conn.close();
  });

  it('handles closing with invalid code', function (done) {
    // Stub out validation checking so we can send the bogus code
    var ErrorCodes = require('ws/lib/ErrorCodes');
    var stub = sandbox.stub(ErrorCodes, 'isValidErrorCode').returns(true);
    toolClient.getSocket().close(123);

    // Make sure to restore isValidErrorCode before next event loop
    stub.restore();

    // Wait for the connection to go away
    connectionManager.once('connection:remove', function () {
      done();
    });
  });

  describe('#ping', function () {
    it('does not throw an exception if connection is closed', function* () {
      conn.close();

      assert.doesNotThrow(function () {
        conn.ping();
      });
    });
  });

  describe('#close', function () {
    it('does not throw an exception if connection is already closed', function* () {
      conn.close();

      assert.doesNotThrow(function () {
        conn.close();
      });
    });
  });

  describe('#checkAlive', function () {
    it('does nothing if connection is already closed', function* () {
      conn.close();

      var setTimeoutSpy = sandbox.spy(global, 'setTimeout');

      // This normally wouldn't happen (timer would alread be removed)
      // This test is just for coverage
      conn.checkAlive();

      // Make sure setTimeout isn't called
      sinon.assert.neverCalledWithMatch(setTimeoutSpy, sinon.match.func, config.pingInterval);
    });
  });

  describe('#resetInactivityTimer', function () {
    beforeEach(function (done) {
      // wipe existing timer before replacing time functions
      if (conn.timerId) {
        clearTimeout(conn.timerId);
        conn.timerId = null;
      }

      clock = sandbox.useFakeTimers();
      done();
    });

    it('sends a ping if connection is idle', function (done) {
      conn.resetInactivityTimer();
      clock.tick(config.pingInterval + 1);

      // ping will come in asynchronously
      toolClient.getSocket().on('ping', function () {
        done();
      });
    });

    it('resets the timer after a pong', function (done) {
      conn.resetInactivityTimer();
      clock.tick(config.pingInterval + 1);

      // pong will come in asynchronously
      conn.ws.on('pong', function () {
        assert.equal(conn.getLastActivityTime(), new Date().getTime());
        done();
      });
    });

    it('resets the timer after a ping (sent from client)', function (done) {
      toolClient.getSocket().ping();

      // ping will come in asynchronously
      conn.ws.on('ping', function () {
        assert.equal(conn.getLastActivityTime(), new Date().getTime());
        done();
      });
    });

    it('kills connections that do not respond to ping', function (done) {
      conn.resetInactivityTimer();

      // disable auto-pong functionality on socket
      toolClient.getSocket().pong = function () {};

      // Make sure we didn't get a pong
      var mock = sandbox.mock(conn);
      mock.expects('resetInactivityTimer').never();

      // Trigger ping
      clock.tick(config.pingInterval + 1);

      toolClient.getSocket().on('close', function (code) {
        assert.equal(code, CloseCode.Timeout);

        mock.verify(); // resetInactivityTimer never called
        done();
      });

      // Advance to ping timeout
      clock.tick(config.pingTimeout + 1);
    });
  });
});
