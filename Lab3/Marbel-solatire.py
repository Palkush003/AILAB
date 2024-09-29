import heapq

class MarbleSolitaireState:
    def init(self, board, empty_cell, path_cost):
        self.board = tuple(board)
        self.empty_cell = empty_cell
        self.path_cost = path_cost

    def lt(self, other):
        return (self.path_cost + self.heuristic()) < (other.path_cost + other.heuristic())

    def heuristic(self):
        return sum(row.count('O') for row in self.board)

def is_valid_move(board, empty_cell, direction):
    row, col = empty_cell

    if direction == "up":
        return row >= 2 and board[row - 1][col] == 'O' and board[row - 2][col] == '.'
    elif direction == "down":
        return row < len(board) - 2 and board[row + 1][col] == 'O' and board[row + 2][col] == '.'
    elif direction == "left":
        return col >= 2 and board[row][col - 1] == 'O' and board[row][col - 2] == '.'
    elif direction == "right":
        return col < len(board[0]) - 2 and board[row][col + 1] == 'O' and board[row][col + 2] == '.'

def apply_move(board, empty_cell, direction):
    row, col = empty_cell
    new_board = [list(row) for row in board]

    if direction == "up":
        new_board[row - 1][col] = '.'
        new_board[row - 2][col] = 'O'
    elif direction == "down":
        new_board[row + 1][col] = '.'
        new_board[row + 2][col] = 'O'
    elif direction == "left":
        new_board[row][col - 1] = '.'
        new_board[row][col - 2] = 'O'
    elif direction == "right":
        new_board[row][col + 1] = '.'
        new_board[row][col + 2] = 'O'

    return ["".join(row) for row in new_board]

def updated_empty_cell_position(empty_cell, direction):
    row, col = empty_cell

    if direction == "up":
        return (row - 2, col)
    elif direction == "down":
        return (row + 2, col)
    elif direction == "left":
        return (row, col - 2)
    elif direction == "right":
        return (row, col + 2)

def goal_condition_met(state):
    center_row = len(state.board) // 2
    center_col = len(state.board[0]) // 2
    return state.board[center_row][center_col] == 'O' and sum(row.count('O') for row in state.board) == 1

def marble_solitaire_solver(initial_state):
    visited_states = set()
    priority_queue = [initial_state]

    while priority_queue:
        current_state = heapq.heappop(priority_queue)

        if current_state.board in visited_states:
            continue

        visited_states.add(current_state.board)

        if goal_condition_met(current_state):
            return current_state

        for direction in possible_moves:
            if is_valid_move(current_state.board, current_state.empty_cell, direction):
                new_board = apply_move(current_state.board, current_state.empty_cell, direction)
                new_empty_cell = updated_empty_cell_position(current_state.empty_cell, direction)
                new_path_cost = current_state.path_cost + 1

                new_state = MarbleSolitaireState(new_board, new_empty_cell, new_path_cost)
                heapq.heappush(priority_queue, new_state)

    return None

# Define your initial board configuration and empty cell position
initial_board = [
    "    OOO    ",
    "    OOO    ",
    "OOOOOOOOOOO",
    "OOOOO.OOOOO",
    "OOOOOOOOOOO",
    "    OOO    ",
    "    OOO    "
]
initial_empty_cell = (3, 4)

initial_state = MarbleSolitaireState(initial_board, initial_empty_cell, 0)

# Define possible moves and helper functions
possible_moves = ["up", "down", "left", "right"]

# Solve the Marble Solitaire
solution = marble_solitaire_solver(initial_state)

# Print the solution path or do further processing as needed
if solution:
    print("Solution found!")
    print("Path cost:", solution.path_cost)
    print("Solution board:")
    for row in solution.board:
        print(row)
else:
    print("No solution found.")