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

var connection = require('./connection');
var config = require('./config');
var util = require('util');
var EventEmitter = require('events').EventEmitter;

function ConnectionManager () {
  EventEmitter.call(this);
  this.allConns = {};
  this.userSessions = {};
}

util.inherits(ConnectionManager, EventEmitter);

// Add a connection to the connection manager
ConnectionManager.prototype.addConnection = function (conn) {
  this.allConns[conn.hashId] = conn;
};

// Register an authenticated connection with a user session
ConnectionManager.prototype.registerConnection = function (conn) {
  if (!conn) throw new Error('missing connection');

  if (!conn.isConnected()) return;

  var userId = conn.getAuthorizedUserId();
  if (!userId) throw new Error('connection does not have an authorized user id');

  var session = this.userSessions[userId];

  if (!session) {
    session = this.userSessions[userId] = {
      userId: userId,
      toolConn: null,
      deviceConns: []
    };
  }

  if (conn.isDevice) {
    session.deviceConns.push(conn);

    if (session.toolConn) {
      // If a tool is connected, hook it up

      // First disconnect old peer
      var oldDevicePeer = session.toolConn.getPeer();
      if (oldDevicePeer && oldDevicePeer !== conn) {
        oldDevicePeer.setPeer(null);
      }

      session.toolConn.setPeer(conn);
      conn.setPeer(session.toolConn);
    }

    // If there's too many device connections, close the oldest
    if (session.deviceConns.length > config.maxDevicesPerAccount) {
      var excessDeviceConn = session.deviceConns.shift();
      excessDeviceConn.close(connection.CloseCode.ConnectionReplaced);
    }
  } else {
    // Only one tool connection can be open at a time
    if (session.toolConn) {
      //console.warn("another tool connecting to same account; closing first");
      session.toolConn.close(connection.CloseCode.ConnectionReplaced);
      session.toolConn = null;
    }

    session.toolConn = conn;

    // If there's any devices, connect the *last* one (most recent)
    if (session.deviceConns.length > 0) {
      var deviceConn = session.deviceConns[session.deviceConns.length - 1];

      conn.setPeer(deviceConn);
      deviceConn.setPeer(conn);
    }
  }

  // Emit event for unit tests
  this.emit('connection:add', conn);
};

// Remove a connection from the connection manager and from any user sessions
ConnectionManager.prototype.removeConnection = function (conn) {
  delete this.allConns[conn.hashId];

  var session = this.userSessions[conn.getAuthorizedUserId()];

  if (session) {
    if (conn.isDevice) {
      session.deviceConns = session.deviceConns.filter(function (c) {
        return c !== conn;
      });
    } else {
      session.toolConn = null;
    }

    var peer = conn.getPeer();
    if (peer) {
      peer.setPeer(null);
    }

    conn.setPeer(null);

    if (!session.toolConn && session.deviceConns.length === 0) {
      // No connections left; delete the record
      delete this.userSessions[session.userId];
    }
  }

  // Emit event for unit tests
  this.emit('connection:remove', conn);
};

ConnectionManager.prototype.getAllConnections = function () {
  var conns = [];
  for (var hashId in this.allConns) {
    conns.push(this.allConns[hashId]);
  }

  return conns;
};

ConnectionManager.prototype.getNumberOfConnections = function () {
  var count = 0;

  /*jshint unused:false */
  for (var key in this.allConns) {
    count++;
  }

  return count;
};

ConnectionManager.prototype.getNumberOfAuthorizedConnections = function () {
  var count = 0;
  for (var userId in this.userSessions) {
    var session = this.userSessions[userId];

    if (session.toolConn) count++;
    count += session.deviceConns.length;
  }
  return count;
};

module.exports = new ConnectionManager();
