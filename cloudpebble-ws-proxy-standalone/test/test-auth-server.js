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

var koa = require('koa');

var app = new koa();

var tokens = {
  'xxx': { userId: 1234 },
  'auth1a': { userId: 1 },
  'auth1b': { userId: 1 },
  'auth2a': { userId: 2 },
  'auth2b': { userId: 2 },
  'userless-token': {}
};

var beforeYield;
var afterYield;

app.use(function* (next) {
  if (beforeYield) yield beforeYield;
  yield next;
  if (afterYield) yield afterYield;
});

app.use(function* () {
  if (this.path === "/oauth/token/info.json") {
    var accessToken = this.query['access_token'];
    var info = tokens[accessToken];

    if (info) {
      this.type = 'json';
      this.body = JSON.stringify({resource_owner_id: {$oid: info.userId}});
    } else {
      return this.throw(401);
    }
  } else {
    return this.throw(404);
  }
});

module.exports.setBeforeAuth = function (generator) {
  beforeYield = generator;
};

module.exports.setAfterAuth = function (generator) {
  afterYield = generator;
};

var server = app.listen(0);

module.exports.app = app;

module.exports.getServerURL = function () {
  return "http://localhost:" + server.address().port;
};
