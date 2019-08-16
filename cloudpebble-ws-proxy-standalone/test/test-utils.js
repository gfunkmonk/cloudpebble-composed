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

var connectionManager = require('../connection-manager');
var config = require('../config');

exports.setupTestServer = function () {
  var testAuthServer = require('./test-auth-server');
  var server = require('../server');

  return function (cb) {
    config.pebbleAuthUrl = testAuthServer.getServerURL();

    server.listen(0, function () {
      toolUrl = "ws://localhost:" + server.address().port + "/tool";
      deviceUrl = "ws://localhost:" + server.address().port + "/device";

      cb(null, {toolUrl: toolUrl, deviceUrl: deviceUrl});
    });
  };
};

exports.cleanupServer = function (server, done) {
  var server = require('../server');

  if (connectionManager.getNumberOfConnections() > 0) {
    var checkAllRemoved = function () {
      if (connectionManager.getNumberOfConnections() === 0) {
        connectionManager.removeListener('connection:remove', checkAllRemoved);
        server.close(done);
      }
    };

    connectionManager.on('connection:remove', checkAllRemoved);
  } else {
    server.close(done);
  }
};

exports.waitForEvent = function (target, event) {
  return new Promise((resolve, reject) => {
    target.once(event, () => {
      resolve();
    });
  });
};
