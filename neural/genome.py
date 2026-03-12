import numpy as np
from neural.neural_network import NeuralNetwork

INPUT_SIZE = 6
HIDDEN_SIZE = 6
OUTPUT_SIZE = 3

class Genome:
    __slots__ = ["network", "fitness"]

    def __init__(self):
        self.network = NeuralNetwork(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
        self.fitness = 0

    def decide(self, inputs):
        output = self.network.forward(inputs)
        return np.argmax(output) # returns 0, 1, or 2

    def mutate(self, rate=0.1):
        for weights in [
            self.network.weights_input_hidden,
            self.network.weights_hidden_output,
            self.network.bias_hidden,
            self.network.bias_output
        ]:
            mask = np.random.rand(*weights.shape) < rate
            weights[mask] += np.random.randn(*weights.shape)[mask]