import numpy as np

class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))

    def train(self, patterns):
        for p in patterns:
            self.weights += np.outer(p, p)
        np.fill_diagonal(self.weights, 0)  # No self-connections

    def recall(self, pattern, steps=10):
        for _ in range(steps):
            pattern = np.sign(self.weights @ pattern)
        return pattern

# Example usage:
size = 100  # 10x10 grid
network = HopfieldNetwork(size)

# Create random binary patterns
patterns = [np.random.choice([-1, 1], size) for _ in range(3)]
network.train(patterns)

# Test recall with noisy input
noisy_pattern = patterns[0] + np.random.choice([-1, 0, 1], size)
noisy_pattern = np.sign(noisy_pattern)
recalled_pattern = network.recall(noisy_pattern)

print("Recalled Pattern:", recalled_pattern)