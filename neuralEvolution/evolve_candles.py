#!/bin/python 
import numpy as np
import theano
theano.config.openmp = True
from keras import backend as K
from devol import DEvol, GenomeHandler


def evolveNetwork(trainCandles, testCandles):

    dataset = ((trainCandles['input'], trainCandles['target']),
               (testCandles['input'], testCandles['target']))

    genome_handler = GenomeHandler(max_conv_layers=2, 
                                   max_dense_layers=3, # includes final dense layer
                                   max_filters=128,
                                   max_dense_nodes=1024,
                                   input_shape=(6, 5, 1),
                                   n_classes=trainCandles['target'].shape[-1])

    devol = DEvol(genome_handler)
    model = devol.run(
        dataset=dataset,
        num_generations=20,
        pop_size=20,
        epochs=5)

    print(model.summary())
