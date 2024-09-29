import numpy as np
import random
import math

PUZZLE_SIZE = 3

# Function to create an initial random state of the puzzle
def create_random_state():
    pieces = list(range(PUZZLE_SIZE * PUZZLE_SIZE))
    random.shuffle(pieces)
    return np.array(pieces).reshape((PUZZLE_SIZE, PUZZLE_SIZE))

# Function to calculate the number of correctly placed pieces
def calculate_cost(state, goal_state):
    return np.sum(state == goal_state)

# Function to swap two pieces in the state
def swap(state):
    x1, y1 = random.randint(0, PUZZLE_SIZE - 1), random.randint(0, PUZZLE_SIZE - 1)
    x2, y2 = random.randint(0, PUZZLE_SIZE - 1), random.randint(0, PUZZLE_SIZE - 1)
    
    # Swap the pieces
    state[x1][y1], state[x2][y2] = state[x2][y2], state[x1][y1]

# Simulated Annealing algorithm
def simulated_annealing(initial_temp, iter_max, min_temp):
    goal_state = np.array([[i * PUZZLE_SIZE + j for j in range(PUZZLE_SIZE)] for i in range(PUZZLE_SIZE)])
    
    current_state = create_random_state()
    current_cost = calculate_cost(current_state, goal_state)

    best_state = np.copy(current_state)
    best_cost = current_cost

    T = initial_temp

    for _ in range(iter_max):
        new_state = np.copy(current_state)
        swap(new_state)
        new_cost = calculate_cost(new_state, goal_state)

        if new_cost > current_cost:
            current_state, current_cost = new_state, new_cost
            
            if new_cost > best_cost:
                best_state, best_cost = new_state, new_cost
        else:
            E = current_cost - new_cost
            pE = math.exp(E / T)
            if random.random() < pE:
                current_state, current_cost = new_state, new_cost

        T *= 0.99
        if T < min_temp:
            break
    
    # Print the best state found
    print("Best State:")
    for row in best_state:
        print(" ".join(f"{val:2d}" for val in row))
    print(f"Best Cost (Correct Pieces): {best_cost}")

if __name__ == "__main__":
    random.seed()
    
    initial_temp = 1000.0
    iter_max = 10000
    min_temp = 0.01
    
    simulated_annealing(initial_temp, iter_max, min_temp)