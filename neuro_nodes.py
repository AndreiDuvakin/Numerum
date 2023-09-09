import random

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


#                          distance|speed
training_input = np.array([[i + 10, i + 5] for i in range(50)])
training_output = np.array([round((i[0] / (int(i[1]) * 1.852)) * 60) for i in range(50)]).T

np.random.seed(1)

synaptic_weight = 2 * np.random.random((2, 50)) - 1

for i in range(10000):
    input_layer = training_input
output = sigmoid(np.dot(input_layer, synaptic_weight))

err = training_output - output
adjustments = np.dot(input_layer.T, err * (output * (1 - output)))

synaptic_weight += adjustments
print(training_input)
print(training_output)
print(output)
