import numpy as np

class NeuralNetwork:
    __slots__ = ["input_size", "hidden_size", "output_size"]

    def __init__(self, input_size, hidden_size, output_size):
        # randomly initialize weights and biases
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.bias_output = np.random.randn(output_size)

    def relu(self, x):
        return np.maximum(0, x)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, inputs):
        # input -> hidden layer
        hidden = self.relu(np.dot(inputs, self.weights_input_hidden) + self.bias_hidden)
        # hidden -> output layer
        output = self.sigmoid(np.dot(hidden, self.weights_hidden_output) + self.bias_output)
        return output