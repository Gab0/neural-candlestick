## What is

Neural-candles, a monolithic python backend to process candlesticks and spit price predictions, based on neural networks.<br>
NNs are various types of layers, Dense, Dropout, LSTM, etc running on top of KERAS/Theano. <br>

Made to be compatible with gekko trading bot running a custom strategy that sends HTTP requests. <br>
Adaptating to other bots should involve only decoding the provided candle from client side (the bot)
and finding a way for the client to send candles via HTTP and expect the prediction.<br>


## How to use

This is an neural network generator that generates various neural network architetures with the objective to predict candlestick prices. <br>
Current version is adapted to a gekko indicator, and at first you need gekko installed.

### Setup

```
1- clone this.

2- instal equirements from PIP.

3- install DEvol from https://github.com/Gab0/devol (this fork is compatible with python 3.7).


```

### Basic Usage

```
1- run mc-server.py, keep it running. it acts as an http server that gets requests
   from gekko indicator and from the cli;

2- run mc-client.py. This step can look like this:

~/neural-candles: $python nc-client.py
candleBank: 0-EVOLVE>load
candleBank: 0-EVOLVE>mode
Candle bank mode 1
candleBank: 1-EVALUATE>load
candleBank: 1-EVALUATE>build

and now we are training the network.

```


### Store Candles

This step is not required, sample dataset is provided.

```
2- run gekko on backtest mode with chosen database on the strategy neuralloader.js.
This will send candlestick data to server, and it will store it in non-permanent fashion.
Pay attention to candle size! should be the same you want to use the system for real trades

3- run some more backtests with more candles from another exchange/asset/currency

4- the command 'save' will save loaded candlesticks

5- the command 'mode' changes the mode to evaluation candle mode, so it listen to candles that will be used as evaluators of the learning process.

6- repeat step 3 and 4 on eval mode; select different candlestick sets

7- you can load saved candles with 'load', for evolution and evaluation candles while at 
corresponding mode;

```

### Use Modes

```
A) STANDALONE 

1- command 'build' will build a default network as specified in neuralGenesis.py

2- command 'evolve' will launch the learning process with loaded candles.

3- command 'test' picks one candle set at random from dataset and predicts it.

B) GEKKO INDICATOR

1- add the indicator to any strategy. it result is the predicted price of candle given loaded, trainded network at the running server.

2- the indicator can send candles to the running server.
```


The actual prediction system is not finished XD. TBD when we have worthwile results on network training.

### Improve

The labelling system is `neuralCandles.preprocessCandles.priceDataset`, this is critical for prediction capability and also easy changeable, just... modify the labels.

### Manifesto :3

The network created has its structure defined according to given parameters at creation time.<br>
This operation is convenitly designed for usage with genetic algorithms.<br>
So we basically test diverse neural network architectures thru genetic algorithm to find which one learns to predict candles faster.<br>
The fitness should be the prediction rate based on a fixed database of candlesticks. <br>
A low EPOCH_NB should be used, we want networks that predict corretly with the least training time.<br>
<br><br>
This is actually a scientific experiment. Are the cryptocoin candles really chaotic behind their skyhigh volatility, therefore unpredictable, or there is a way to beat da system?<br>
In my vision trading bots currently are not sufficiently consistent to be labeled as sucessful. <br>
Gekko is a good framework where many strategies found over the internet are able to fail.<br>
Maybe some people actually profit on live trading, keeping their strats in secret...<br>
<br>
Some strategies for gekko utilize neuralnetworks. <br>
Some say they are scam, others enjoy those 6^e¹¹ percent profit on backtests that usually happen. <br>
They are based on simple NN structures and are not known to profit consistently on live trading.

So this software is an effort to check if candlesticks are scientifically, consistently, predictable or not.<br><br>

```
TODO:

- Japonicus integration - genetic algorithm evolves neural shape parameters;
- Candle processing method for training (gekko database/sqlite & from http requests)

```

## Changelog


```
v0.3

- using DEvol for nn topology search.
```
