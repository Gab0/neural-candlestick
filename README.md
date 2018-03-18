### What is

Neural-candles, a monolithic python backend to process candlesticks and spit price predictions, based on neural networks.
NNs are LSTMs running on top of KERAS/Theano.

Made to be compatible with gekko trading bot running a custom strategy that sends HTTP requests. Adaptating to other bots should involve only decoding the provided candle from server side (this) and finding a way for the client to send candles via HTTP and expect the prediction.

### Goals

The network created is initially amorphous, its structure variates according to given parameters at creation time. An operation onvenitly designed for usage with genetic algorithms.
So we basically test diverse neural network architectures thru GA.
The fitness should be the prediction rate based on a fixed database of candlesticks. A low EPOCH_NB should be used, we want networks that predict corretly with the least training time.

This is actually a scientific experiment. Are the cryptocoin candles really chaotic behind their skyhigh volatility, and unpredictable, or there is a way to beat da system?
In my vision no trading bots currently are sufficiently consistent to be labeled as sucessful. Gekko is a good framework where many strategies found over the internet are able to fail. Maybe people actually profit on live trading, keeping their strats in secret.

Some strategies for gekko utilize neuralnetworks. <br>
Some say they are scam, some enjoy the 6^e¹¹ percent profit on backtests. They are based on simple NN structures and are not known to profit consistently on live trading.

So this software is an effort to check if candlesticks are scientifically, consistently predictable or not.<br><br>

```
TODO:

- Plastical neural network, shape from parameters;
- Japonicus integration - genetic algorithm evolves neural shape parameters;
- Candle processing method for training (gekko database/sqlite & from http requests)

```



## Milestones


```

v0.01 

- Genesis
- HTTP dummy requests (testing most efficient lib/method)


```
