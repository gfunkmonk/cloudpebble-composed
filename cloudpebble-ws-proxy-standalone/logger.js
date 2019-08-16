'use strict';

var bunyan = require('bunyan');

module.exports = bunyan({
  name: require('./package.json').name
});
