import numpy as np

# Generate synthetic data
np.random.seed(0)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

# Initialize parameters
theta = np.random.randn(2, 1)

# Add bias term to input
X_b = np.c_[np.ones((100, 1)), X]

# Define cost function (Mean Squared Error)
def cost_function(theta, X, y):
    m = len(y)
    predictions = X.dot(theta)
    cost = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
    return cost

# Define gradient of cost function
def gradient(theta, X, y):
    m = len(y)
    grad = (1 / m) * X.T.dot(X.dot(theta) - y)
    return grad

# Define gradient descent algorithm
def gradient_descent(X, y, theta, learning_rate, n_iterations):
    cost_history = []
    for iteration in range(n_iterations):
        grad = gradient(theta, X, y)
        theta = theta - learning_rate * grad
        cost = cost_function(theta, X, y)
        cost_history.append(cost)
    return theta, cost_history

# Perform gradient descent
learning_rate = 0.01
n_iterations = 1000
theta_optimal, cost_history = gradient_descent(X_b, y, theta, learning_rate, n_iterations)

print ('Optimal theta:', theta_optimal)
print ('Optimal cost:', cost_history[-1])
