//nncandle indicator, the entrypoint for neural-candlestick;
//


var request = require('then-request');
var request = require('then-request');


const querystring = require('querystring');

var Indicator = function(settings) {

    this.input = 'candle';
    this.storeCandle = settings.storeCandle || false;

    this.Host = settings.Host;
    this.Port = settings.Port;

    this.candles = [];


    this.candlePackSize = settings.candlePackSize;
    this.futurePredictionPoint = settings.futurePredictionPoint;

    this.candleHistorySize = this.candlePackSize +
        this.futurePredictionPoint;
}

Indicator.prototype.sendCandle = function(candle) {
    // Build the post string from an object
    //console.log(candle);

    //const data = querystring.stringify(candle);

    // An object of options to indicate where to post to
    let Response = '';
    let URL = "http://" + this.Host + ':' + this.Port;
    if (this.storeCandle){
        URL += "/candleinput";
    }
    else {
        URL += "/predict";
    }

    request('POST', URL, {json: {candles: candle}}).done(function(res){
        var response = res.getBody();
        //console.log(response);
    });

}



Indicator.prototype.update = function(candle) {

    this.candles.push(candle);


    if (this.candles.length > this.candleHistorySize)
    {
        this.candles.shift();

        var candleEnsemble = this.candles.slice(0, this.candlePackSize);

        candleEnsemble.push(candle);

        this.sendCandle(candleEnsemble);
    }

    this.result = 0;
}


module.exports = Indicator;
