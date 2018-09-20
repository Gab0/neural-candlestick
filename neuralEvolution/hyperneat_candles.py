#!/bin/python

import neat
import neat.nn
import pickle
from pureples.shared.visualize import draw_net
from pureples.shared.substrate import Substrate
from pureples.hyperneat.hyperneat import create_phenotype_network
from pureples.es_hyperneat.es_hyperneat import ESNetwork

# Network inputs and expected outputs.
input_coordinates = [(0, 1) for k in range(5)]
output_coordinates = [(0.0, 1.0)]


substrate = Substrate(input_coordinates, output_coordinates)

params = {
    "initial_depth": 1,
    "max_depth": 2,
    "variance_threshold": 0.03,
    "band_threshold": 0.3,
    "iteration_level": 1,
    "division_threshold": 0.5,
    "max_weight": 8.0,
    "activation": "sigmoid"
}


def eval_fitness(genomes, config):
    for g, genome in genomes:
        cppn = neat.nn.FeedForwardNetwork.create(genome, config)
        network = ESNetwork(substrate, cppn, params)
        net = network.create_phenotype_network()

        sum_error = 0.0
        direction_error = 0

        for inputs, expected in zip(IN, OUT):
            net.reset()
            for candle in inputs:
                print(candle)
                output = net.activate(candle)

            out, exp = output[0], expected[0][3]
            sum_error += abs(out - exp)

            if ((out - exp) > 0) != ((candle[3] - exp) > 0):
                direction_error += 3
            print(out)
            # print(exp)
        # print(direction_error)
        genome.fitness = 1 - sum_error - direction_error


# create the population;
def run(config, gens):
    pop = neat.population.Population(config)
    stats = neat.statistics.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.reporting.StdOutReporter(True))

    winner = pop.run(eval_fitness, gens)
    print("hyperneat candle evolution is done.")
    return winner, stats


# If run as script.
def evolveNeurals(configPath, X, Y):
    # using globals xd
    global IN
    IN = X
    global OUT
    OUT = Y

    config = neat.config.Config(neat.genome.DefaultGenome,
                                neat.reproduction.DefaultReproduction,
                                neat.species.DefaultSpeciesSet,
                                neat.stagnation.DefaultStagnation,
                                configPath)

    winner = run(config, 1000)[0]
    print('\nBest genome:\n{!s}'.format(winner))

    # Verify network output against training data.
    print('\nOutput:')
    cppn = neat.nn.FeedForwardNetwork.create(winner, config)
    winner_net = create_phenotype_network(cppn, substrate)

    """
    for inputs, expected in zip(xor_inputs, xor_outputs):
        new_input = inputs + (1.0,)
        winner_net.reset()
        for i in range(activations):
            output = winner_net.activate(new_input)
        showOutputs = (inputs, expected, output)
        print("  input %.4f, expected output %.4f, got %.4f" % showOutputs)
    """


def saveNetwork(cppn, winner_net):
    # Save CPPN if wished reused and draw it to file along with the winner.
    with open('hyperneat_xor_cppn.pkl', 'wb') as output:
        pickle.dump(cppn, output, pickle.HIGHEST_PROTOCOL)
    draw_net(cppn, filename="hyperneat_xor_cppn")
    draw_net(winner_net, filename="hyperneat_xor_winner")


def loadNetwork():
    n = pickle.load('hyperneat')
