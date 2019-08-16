'use strict';

require('dotenv').load();

// Port
exports.port = parseInt(process.env.PORT, 10);

// Base URL for Pebble auth server
exports.pebbleAuthUrl = process.env.PEBBLE_AUTH_URL;

// How frequently to send a ping to the websocket client
// Heroku requires this to be less than 55 seconds
exports.pingInterval =
  (parseInt(process.env.PING_INTERVAL_SECONDS, 10) || 45) * 1000;

// How long to wait for a ping response
// This should be moderately high in case the connection
// is busy transferring a large file, which Heroku will
// allow (since data is still being transferred)
// but might delay the ping.
exports.pingTimeout =
  (parseInt(process.env.PING_TIMEOUT_SECONDS, 10) || 120) * 1000;

// Max number of device connections per account
exports.maxDevicesPerAccount =
  parseInt(process.env.MAX_DEVICE_CONNECTIONS, 10) || 10;
