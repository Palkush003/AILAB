from collections import deque

class State:
    def __init__(self, missionaries_left, cannibals_left, boat):
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.boat = boat
        self.missionaries_right = 3 - missionaries_left
        self.cannibals_right = 3 - cannibals_left

    def is_valid(self):
        # Check that missionaries are not outnumbered on either side
        if (self.missionaries_left >= 0 and self.missionaries_right >= 0 and
            self.cannibals_left >= 0 and self.cannibals_right >= 0 and
            (self.missionaries_left == 0 or self.missionaries_left >= self.cannibals_left) and
            (self.missionaries_right == 0 or self.missionaries_right >= self.cannibals_right)):
            return True
        return False

    def is_goal(self):
        return self.missionaries_left == 0 and self.cannibals_left == 0 and self.boat == 1

    def __eq__(self, other):
        return (self.missionaries_left == other.missionaries_left and 
                self.cannibals_left == other.cannibals_left and
                self.boat == other.boat)

    def __hash__(self):
        return hash((self.missionaries_left, self.cannibals_left, self.boat))

def dfs():
    initial_state = State(3, 3, 0)
    if initial_state.is_goal():
        return initial_state
    
    stack = [(initial_state, [])]  # Stack stores state and path to reach that state
    visited = set()
    visited.add(initial_state)
    # Possible boat actions: (M, C)
    actions = [(2, 0), (1, 0), (1, 1), (0, 1), (0, 2)]
    
    while stack:
        current_state, path = stack.pop()
        
        if current_state.is_goal():
            return path + [current_state]
        
        # Generate next states based on possible actions
        for action in actions:
            if current_state.boat == 0:
                next_state = State(current_state.missionaries_left - action[0],
                                   current_state.cannibals_left - action[1],
                                   1)
            else:
                next_state = State(current_state.missionaries_left + action[0],
                                   current_state.cannibals_left + action[1],
                                   0)
            
            if next_state.is_valid() and next_state not in visited:
                visited.add(next_state)
                stack.append((next_state, path + [current_state]))

    return None
# Printing the solution
solution = dfs()
if solution:
    for step, state in enumerate(solution):
        print(f"Step {step}: {state.missionaries_left} missionaries, {state.cannibals_left} cannibals on the left; boat on {'left' if state.boat == 0 else 'right'}")
else:
    print("No solution found")
