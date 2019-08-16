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
var connection = require('../connection');
var MessageType = connection.MessageType;
var assert = require('assert');
var co = require('co');

function TestClient (ws) {
  var messageCb = null;
  var queued = [];
  var closeCode = undefined;
  var closeCb;

  ws.on('message', function (message) {
    if (messageCb) {
      cb = messageCb;
      messageCb = null;

      cb(null, message);
    } else {
      queued.push(message);
    }
  });

  ws.on('close', function (code) {
    closeCode = code;
    if (closeCb) {
      closeCb(null, code);
      closeCb = null;
    }
  });

  this.send = function (message) {
    ws.send(message);
  };

  this.close = function (code) {
    ws.close(code);
  };

  this.getSocket = function () {
    return ws;
  };

  this.sendAccessToken = function (token) {
    if (!token) {
      throw new Error('sendAccessToken requires a token');
    }

    this.send(createAuthMessage(token));
  };

  this.authorize = function* (token) {
    this.sendAccessToken(token);
    var message = yield this.nextMessage();

    assert.equal(MessageType.ProxyAuthentication, message[0]);
    assert.equal(0x00, message[1], "authorization not successful");
  };

  this.failToAuthorize = function* (token) {
    this.sendAccessToken(token);
    var message = yield this.nextMessage();

    assert.equal(MessageType.ProxyAuthentication, message[0]);
    assert.equal(0x01, message[1], "authorization should have failed");
  };

  this.nextMessage = function () {
    return function (cb) {
      if (queued.length > 0) {
        cb(null, queued.shift());
      } else {
        if (messageCb) {
          cb(new Error("can't call nextMessage before last one returns"));
        }

        messageCb = cb;
      }
    };
  };

  this.waitForClose = function () {
    return function (cb) {
      if (closeCode !== undefined) {
        cb(null, closeCode);
      } else {
        closeCb = cb;
      }
    };
  };
}

function createAuthMessage(token) {
  var buf = new Buffer(2 + token.length);
  buf[0] = MessageType.ProxyAuthentication;
  buf[1] = token.length;
  buf.write(token, 2, undefined, 'ascii');
  return buf;
}

var TestClientManager = function () {
  this.clients = [];
};

TestClientManager.prototype.createTestClient = function (url) {
  var self = this;

  return function (cb) {
    var ws = new WebSocket(url);

    ws.on('open', function () {
      var client = new TestClient(ws);
      self.clients.push(client);
      cb(null, new TestClient(ws));
    });

    ws.on('error', function (err) {
      cb(err);
    });
  };
};

TestClientManager.prototype.closeAll = function () {
  var clients = this.clients;
  this.clients = [];

  clients.forEach(function (client) {
    client.close();
  });
};

module.exports.TestClientManager = TestClientManager;
