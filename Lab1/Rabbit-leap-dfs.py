# Initial and goal states
initial_state = "WWW_EEE"
goal_state = "EEE_WWW"

# Function to print the states
def print_state(state):
    print(state)

# Function to check if a move is valid
def is_valid_move(from_idx, to_idx, state):
    if to_idx < 0 or to_idx >= len(state):
        return False
    if state[to_idx] == 'E' and state[from_idx] == 'W':
        return False
    return abs(to_idx - from_idx) == 1 or abs(to_idx - from_idx) == 2

# Function to generate all possible next states
def get_next_states(state):
    next_states = []
    empty_index = state.find('_')
    for i in range(len(state)):
        if state[i] != '_':
            if is_valid_move(i, empty_index, state):
                new_state = list(state)
                new_state[empty_index], new_state[i] = new_state[i], new_state[empty_index]
                next_states.append("".join(new_state))
    return next_states

# DFS to find the path to the goal state using a stack
def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()
    visited.add(start)

    while stack:
        current_state, path = stack.pop()

        if current_state == goal:
           print(f"The Number of steps to find optimal solution is {len(visited)}")
           return path

        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                new_path = path + [next_state]
                stack.append((next_state, new_path))

    return []

if __name__ == "__main__":
    solution = dfs(initial_state, goal_state)

    if solution:
        print("Solution found:")
        for state in solution:
            print_state(state)
    else:
        print("No solution.found.")