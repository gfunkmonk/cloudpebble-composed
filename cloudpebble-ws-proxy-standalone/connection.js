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

'use strict';

var co = require('co');
var auth = require('./auth');
var connectionManager = require('./connection-manager');
var config = require('./config');
var logger = require('./logger');

var nextHashId = 1; // global counter; used to give a unique id to connections

var MessageType = module.exports.MessageType = {
  WatchToPhone: 0x00,
  PhoneToWatch: 0x01,
  ProxyConnectionStatusUpdate: 0x08,
  ProxyAuthentication: 0x09
};

var CloseCode = module.exports.CloseCode = {
  // Standard codes: see http://tools.ietf.org/html/rfc6455#section-7.4.1
  // The standard does not give names to these codes; the names here
  // are just to make it easier to cross-reference in the code.
  Done: 1000,
  Shutdown: 1001,
  ProtocolError: 1002,
  UnsupportedDataType: 1003,
  InvalidMessage: 1008,
  MessageTooLarge: 1009,
  InternalError: 1011,

  // These codes are custom to our application
  AuthorizationRequired: 4401,
  Timeout: 4408,
  ConnectionReplaced: 4409
};

var ProxyConnectionStatus = module.exports.ProxyConnectionStatus = {
  Connected: 0xFF,
  Disconnected: 0x00,
};

var ProxyAuthenticationResult = module.exports.ProxyAuthenticationResult = {
  Success: 0x00,
  Failed: 0x01
};

function Connection (ws, isDevice) {
  this.closed = false;
  this.ws = ws;
  this.isDevice = isDevice;
  this.needsAuth = true;
  this.userId = null;
  this.peer = null;
  this.hashId = nextHashId++;
  this.lastActivityTime = new Date().getTime();

  ws.on('message', this.handleMessage.bind(this));
  ws.on('error', this.handleError.bind(this));
  ws.on('close', this.handleClose.bind(this));
  ws.on('ping', this.handlePing.bind(this));
  ws.on('pong', this.handlePong.bind(this));

  connectionManager.addConnection(this);

  this.resetInactivityTimer();
}

module.exports.Connection = Connection;

Connection.prototype.handleMessage = function (message) {
  if (!(message instanceof Buffer)) {
    this.close(CloseCode.UnsupportedDataType);
    return;
  }

  this.resetInactivityTimer();

  if (this.needsAuth) {
    // TYPE (1 byte), PAYLOAD
    var type = message[0];

    if (type === MessageType.ProxyAuthentication) {
      this.handleAuthMessage(message);
    } else {
      this.close(CloseCode.AuthorizationRequired);
      return;
    }
  } else {
    if (this.peer) {
      this.peer.sendMessage(message);
    } // otherwise, message gets dropped on the floor
  }
};

Connection.prototype.handleAuthMessage = co.wrap(function* (message) {
  var length = message[1];
  var accessToken = message.toString('ascii', 2, length + 2);

  try {
    // logger.trace('authenticating user using token ' + accessToken);

    this.userId = yield auth.getUserId(accessToken);
    this.needsAuth = false;

    // logger.debug({userId: this.userId}, 'authenticated user: ' + this.userId);

    this.sendMessage([
        MessageType.ProxyAuthentication
      , ProxyAuthenticationResult.Success
    ]);

    connectionManager.registerConnection(this);
  } catch (e) {
    logger.warn(e, 'error authorizing auth token');

    // Invalid access token
    this.sendMessage([
        MessageType.ProxyAuthentication
      , ProxyAuthenticationResult.Failed
    ]);
  }
});

Connection.prototype.handleError = function (err) {
  logger.warn(err, 'error in connection');
  this.ws.terminate();
  this.finishClose();
};

Connection.prototype.handleClose = function () {
  // separate function to make it easier to test
  this.finishClose();
};

Connection.prototype.finishClose = function () {
  if (!this.closed) {
    this.closed = true;

    /* istanbul ignore else */
    if (this.timerId) {
      clearTimeout(this.timerId);
      this.timerId = null;
    }

    connectionManager.removeConnection(this);
  }
};

Connection.prototype.isConnected = function () {
  return !this.closed && this.ws.readyState === 1;
};

Connection.prototype.sendMessage = function (message) {
  if (!this.isConnected()) { // not open
    return;
  }

  if (message instanceof Buffer) {
    this.ws.send(message);
  } else {
    this.ws.send(new Buffer(message));
  }
};

Connection.prototype.getPeer = function () {
  return this.peer;
};

Connection.prototype.setPeer = function (peer) {
  var oldPeer = this.peer;

  if (oldPeer === peer) {
    return;
  }

  if (!this.closed) {
    if (oldPeer) {
      this.sendPeerDisconnected();
    }

    this.sendPeerConnected();
  }

  this.peer = peer;
};

Connection.prototype.sendPeerConnected = function () {
  this.sendMessage([
      MessageType.ProxyConnectionStatusUpdate
    , ProxyConnectionStatus.Connected
  ]);
};

Connection.prototype.sendPeerDisconnected = function () {
  this.sendMessage([
      MessageType.ProxyConnectionStatusUpdate
    , ProxyConnectionStatus.Disconnected
  ]);
};

Connection.prototype.getAuthorizedUserId = function () {
  return this.userId;
};

Connection.prototype.close = function (code) {
  if (this.closed) return;

  this.ws.close(code);

  // Handle close immediately to avoid race conditions in our internal state.
  // The finishClose method will make sure it does not get called twice.
  this.finishClose();
};

Connection.prototype.ping = function () {
  if (!this.isConnected()) return;

  this.ws.ping();
};

Connection.prototype.handlePing = function () {
  this.resetInactivityTimer();
};

Connection.prototype.handlePong = function () {
  this.resetInactivityTimer();
};

Connection.prototype.resetInactivityTimer = function () {
  this.lastActivityTime = new Date().getTime();

  if (this.timerId) {
    clearTimeout(this.timerId);
  }

  this.timerId = setTimeout(this.checkAlive.bind(this), config.pingInterval);
};

Connection.prototype.checkAlive = function () {
  if (!this.isConnected()) return;

  // If this timer isn't reset by network activity (such as a pong)
  // then assume that the connection died
  this.timerId = setTimeout(this.timedOut.bind(this), config.pingTimeout);

  this.ping();
};

Connection.prototype.timedOut = function () {
  this.close(CloseCode.Timeout);
};

Connection.prototype.getLastActivityTime = function () {
  return this.lastActivityTime;
};
