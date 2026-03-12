"""
Represents a neural network, the dino's brain.

@author: Jambaldorj Munkhsoyol
"""

import numpy as np

class NeuralNetwork:
    """
    A simple 3-layer neural network: input -> hidden -> output.
    """

    __slots__ = ["weights_input_hidden", "weights_hidden_output", "bias_hidden", "bias_output"]

    def __init__(self, input_size, hidden_size, output_size):
        """
        Build a new network with random weights and biases.

        np.random.randn() fills an array with random numbers from a normal
        distribution (most values between -1 and 1, centred around 0).
        These random starting values mean each dino in the first generation
        behaves differently. Some will get lucky and survive longer,
        and those genes get passed on.

        @param input_size: number of input neurons (7)
        @param hidden_size: number of hidden neurons (6)
        @param output_size: number of output neurons (3)
        """
        # randomly initialize weights and biases
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)   # controls how inputs influence hidden neurons
        self.weights_hidden_output = np.random.randn(hidden_size, output_size) # controls how hidden neurons influence outputs
        self.bias_hidden = np.random.randn(hidden_size)                        # a nudge added to each hidden neuron before activation
        self.bias_output = np.random.randn(output_size)                        # a nudge added to each output neuron before activation

    def relu(self, x):
        """
        ReLU (Rectified Linear Unit) activation function.

        Turns any negative number into 0, leaves positive numbers unchanged.
        Applied to the hidden layer so neurons that receive weak or negative
        signals simply stay silent (output 0) rather than passing noise forward.
        """
        return np.maximum(0, x)

    def sigmoid(self, x):
        """
        Sigmoid activation function.

        Squashes any number into the range (0, 1).
        Applied to the output layer so all three action scores are on the
        same 0–1 scale, making argmax in genome.py a fair comparison.
        """
        return 1 / (1 + np.exp(-x))

    def forward(self, inputs):
        """
        Run one set of inputs through the network and return 3 output scores.

        How each layer works:
            1. Multiply every input by its weight for each neuron (np.dot)
            2. Add the neuron's bias
            3. Pass the result through an activation function (relu or sigmoid)
            The output of one layer becomes the input to the next.

        @param inputs: list or np.array of 7 floats, all normalized to roughly 0–1
        @returns: np.array of 3 floats, scores for [jump, duck, do nothing]
        """
        # input -> hidden layer
        hidden = self.relu(np.dot(inputs, self.weights_input_hidden) + self.bias_hidden)
        # hidden -> output layer
        output = self.sigmoid(np.dot(hidden, self.weights_hidden_output) + self.bias_output)
        return output