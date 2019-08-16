cloudpebble-ws-proxy
====================

Proxy service that routes WebSocket messages between [CloudPebble](https://github.com/pebble/cloudpebble) and
the Pebble iOS/Android apps to enable the developer connection functionality.

### Setup

Copy .env.sample to .env and adjust the values as needed.

Node 4+ is required. Get it from http://nodejs.org/dist/

Install npm modules:

    npm install

To run:

    npm start

Or:

    node start.js

### Deployment

- Since `cloudpebble-ws-proxy` relays messages internally between websockets,
  there must only be one server instance running at a time.
- Load balancers must support websockets or raw TCP proxying. If there's a
  socket timeout, PING_INTERVAL_SECONDS should be set to a value lower than
  the connection timeout (55 seconds for Heroku).

### Usage

- Tools (CloudPebble IDE) should connect to /tool, e.g. ws://server.ip/tool

- Devices (iOS, Android) should connect to /device, e.g. ws://server.ip/device

- The first message sent over the websocket should be a proxy authorization request:

    [0x09, length of token (1 byte), access token bytes (max 255 bytes)]

- The proxy will respond with [0x09, 0x00] for success or [0x09, 0x01] for failure

- Anything sent over the connection prior to getting an authorization response will be lost.

#### Limits

- Only one tool connection can be open at a time. If another tool connects to a given account,
  the previous connection will be closed with error code 4408.

- Multiple device connections can be open at time. The most recent device to connect to an
  account will be the active connection. If another device connects, the tool connection will
  get a "disconnected" proxy status message, followed by a "connected" proxy status message,
  and the old device will get a "disconnected" proxy status message.

### Development

#### running tests

- `make test` runs tests
- `make test-cov` runs tests + test coverage
- `make open-cov` opens test coverage results in your browser
