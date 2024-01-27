import numpy as np

# Define the shape of weights and biases
input_size = 784  # Example: input size for an image with shape (28, 28) flattened to 784
hidden_size = 256
output_size = 10

# Initialize weights and biases for a neural network
weights_hidden = np.around(np.random.uniform(-1, 1, (input_size, hidden_size)), decimals=2)
biases_hidden = np.around(np.random.uniform(-1, 1, (1, hidden_size)), decimals=2)

weights_output = np.around(np.random.uniform(-1, 1, (hidden_size, output_size)), decimals=2)
biases_output = np.around(np.random.uniform(-1, 1, (1, output_size)), decimals=2)

# Check the initialized weights and biases
print("Initialized weights for the hidden layer:")
print(weights_hidden)
print("\nInitialized biases for the hidden layer:")
print(biases_hidden)
print("\nInitialized weights for the output layer:")
print(weights_output)
print("\nInitialized biases for the output layer:")
print(biases_output)
