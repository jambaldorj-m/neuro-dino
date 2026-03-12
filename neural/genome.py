"""
Bundles the dino's brain and the score together

@author: Jambaldorj Munkhsoyol
"""

import numpy as np
from neural.neural_network import NeuralNetwork

INPUT_SIZE = 7
HIDDEN_SIZE = 6
OUTPUT_SIZE = 3

class Genome:
    """
    One individual in the population — a brain paired with a fitness score.
    """

    __slots__ = ["network", "fitness"]

    def __init__(self):
        """
        Create a new genome with a randomly initialized brain and zero fitness.
        """
        self.network = NeuralNetwork(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE) # the dino's brain, holds all weights and biases
        self.fitness = 0                                                   # how well this dino performed last generation

    def decide(self, inputs):
        """
        Ask the brain what action to take given the current game state.

        Runs the inputs through the neural network (forward pass), then picks
        whichever of the 3 output scores is highest.

        @param inputs: list of 7 floats from get_inputs() in main.py
        @returns: 0 (jump), 1 (duck), or 2 (do nothing)
        """
        output = self.network.forward(inputs)
        return np.argmax(output)

    def mutate(self, rate=0.1):
        """
        Randomly nudge some weights and biases in the brain.

        How it works for each weight array:
            1. Create a boolean mask — True at each position where mutation fires
            2. Generate a full array of random nudges the same shape as the weights
            3. Apply nudges only where the mask is True
        """
        for weights in [
            self.network.weights_input_hidden,
            self.network.weights_hidden_output,
            self.network.bias_hidden,
            self.network.bias_output
        ]:
            mask = np.random.rand(*weights.shape) < rate
            weights[mask] += np.random.randn(*weights.shape)[mask]