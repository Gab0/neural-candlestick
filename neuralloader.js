const _ = require('lodash');
const http = require('http');
const log = require('../core/log');

const strat = {};


strat.init = function() {
    this.age = 0;

    // Set up the request
    this.Host = 'localhost';
    this.Port = '5000';

    const nnsettings = {
        Host: 'localhost',
        Port: '5000',
        candlePackSize: 6,
        futurePredictionPoint: 3,
        storeCandle: true
    };

    this.addIndicator('NNC', 'nncandle', nnsettings);

};

strat.update = function(candle) {

    this.age++;
};

strat.log = _.noop;
strat.check = _.noop;

module.exports = strat;

