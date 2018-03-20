### What is

Neural-candles, a monolithic python backend to process candlesticks and spit price predictions, based on neural networks.<br>
NNs are various types of layers, Dense, Dropout, LSTM, etc running on top of KERAS/Theano. <br>

Made to be compatible with gekko trading bot running a custom strategy that sends HTTP requests. <br>
Adaptating to other bots should involve only decoding the provided candle from client side (the bot)
and finding a way for the client to send candles via HTTP and expect the prediction.<br>

### Goals

The network created is initially amorphous, its structure variates according to given parameters at creation time.<br>
An operation convenitly designed for usage with genetic algorithms.<br>
So we basically test diverse neural network architectures thru GA.<br>
The fitness should be the prediction rate based on a fixed database of candlesticks. <br>
A low EPOCH_NB should be used, we want networks that predict corretly with the least training time.<br>
<br>
This is actually a scientific experiment. Are the cryptocoin candles really chaotic behind their skyhigh volatility, and unpredictable, or there is a way to beat da system?
In my vision trading bots currently are not sufficiently consistent to be labeled as sucessful. <br>
Gekko is a good framework where many strategies found over the internet are able to fail.<br>
Maybe some people actually profit on live trading, keeping their strats in secret.<br>
<br>
Some strategies for gekko utilize neuralnetworks. <br>
Some say they are scam, others enjoy the 6^e¹¹ percent profit on backtests. <br>
 They are based on simple NN structures and are not known to profit consistently on live trading.

So this software is an effort to check if candlesticks are scientifically, consistently, predictable or not.<br><br>

```
TODO:

- Plastical neural network, shape from parameters;
- Japonicus integration - genetic algorithm evolves neural shape parameters;
- Candle processing method for training (gekko database/sqlite & from http requests)

```

## Changelog


```
v0.02

- nicer readme
- network creation works
- HTTP requests works

v0.01 

- Genesis
- HTTP dummy requests (testing most efficient lib/method)
- nice readme XD
- nothing works

```
