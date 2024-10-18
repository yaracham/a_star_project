import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import heapq
import time
import tracemalloc
from collections import deque
import heapq

# Disjoint Pattern Database
# Pattern 1: Tiles 1, 2, 3, 4
# Pattern 2: Tiles 5, 6, 7, 8

# Goal states for both patterns
goal_pattern1 = np.array([[1, 2, 3], [4, 0, 0], [0, 0, 0]])  # Only 1, 2, 3, 4 are considered
goal_pattern2 = np.array([[0, 0, 0], [0, 5, 6], [7, 8, 0]])  # Only 5, 6, 7, 8 are considered

# Precomputed pattern database (in practice, this would be done offline and stored in a file)
pattern_db1 = {}
pattern_db2 = {}

# Utility function to hash a pattern state into a tuple for easy lookup
def pattern_hash(state, pattern):
    return tuple(state[state != 0])

# BFS to create the pattern database
def bfs_pattern_db(goal_state):
    queue = deque([(goal_state.copy(), 0)])  # (state, cost)
    visited = set()
    pattern_db = {}

    while queue:
        current_state, cost = queue.popleft()
        state_hash = pattern_hash(current_state, current_state)

        if state_hash not in visited:
            visited.add(state_hash)
            pattern_db[state_hash] = cost

            # Generate all possible legal moves (move the blank space)
            blank_pos = np.argwhere(current_state == 0)[0]
            row, col = blank_pos

            # Move up
            if row > 0:
                new_state = current_state.copy()
                new_state[row, col], new_state[row - 1, col] = new_state[row - 1, col], new_state[row, col]
                queue.append((new_state, cost + 1))

            # Move down
            if row < 2:
                new_state = current_state.copy()
                new_state[row, col], new_state[row + 1, col] = new_state[row + 1, col], new_state[row, col]
                queue.append((new_state, cost + 1))

            # Move left
            if col > 0:
                new_state = current_state.copy()
                new_state[row, col], new_state[row, col - 1] = new_state[row, col - 1], new_state[row, col]
                queue.append((new_state, cost + 1))

            # Move right
            if col < 2:
                new_state = current_state.copy()
                new_state[row, col], new_state[row, col + 1] = new_state[row, col + 1], new_state[row, col]
                queue.append((new_state, cost + 1))

    return pattern_db

# Create the pattern databases
# pattern_db1 = bfs_pattern_db(goal_pattern1)
# pattern_db2 = bfs_pattern_db(goal_pattern2)


# 8-Puzzle Class
class EightPuzzle:
    def __init__(self, initial_state):
        self.state = np.array(initial_state)
        self.blank_pos = np.argwhere(self.state == 0)[0]

    def move(self, direction):
        """Move the blank tile in a given direction if possible."""
        row, col = self.blank_pos
        if direction == 'up' and row > 0:
            self._swap((row, col), (row - 1, col))
        elif direction == 'down' and row < 2:
            self._swap((row, col), (row + 1, col))
        elif direction == 'left' and col > 0:
            self._swap((row, col), (row, col - 1))
        elif direction == 'right' and col < 2:
            self._swap((row, col), (row, col + 1))

    def _swap(self, pos1, pos2):
        """Swap two positions in the puzzle."""
        self.state[tuple(pos1)], self.state[tuple(pos2)] = self.state[tuple(pos2)], self.state[tuple(pos1)]
        self.blank_pos = pos2  # Update the blank position

    def is_solved(self):
        """Check if the puzzle is solved."""
        return np.array_equal(self.state, np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]))

    def copy(self):
        """Return a copy of the current puzzle."""
        return EightPuzzle(self.state.copy())

    def legal_moves(self):
        """Returns a list of legal moves from the current state."""
        row, col = self.blank_pos
        moves = []
        if row > 0:
            moves.append('up')
        if row < 2:
            moves.append('down')
        if col > 0:
            moves.append('left')
        if col < 2:
            moves.append('right')
        return moves

    def result(self, move):
        """Returns the resulting state from applying a move."""
        new_puzzle = self.copy()
        new_puzzle.move(move)
        return new_puzzle

    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

    def __hash__(self):
        return hash(self.state.tobytes())

    def __str__(self):
        """String representation of the puzzle state."""
        return '\n'.join([' '.join(map(str, row)) for row in self.state]) + '\n'
    
    def __lt__(self, other):
        return manhattan_distance(self) < manhattan_distance(other)
    
def is_solvable(puzzle):
    # Flatten the puzzle into a 1D list, excluding the blank (0)
    flattened_puzzle = [tile for row in puzzle for tile in row]
    
    # Count the number of inversions
    inversions = 0
    for i in range(len(flattened_puzzle)):
        for j in range(i + 1, len(flattened_puzzle)):
            if flattened_puzzle[i] > flattened_puzzle[j] and flattened_puzzle[j] != 0:
                inversions += 1

    # Return True if the number of inversions is even
    return inversions % 2 == 0


# BFS Solver
def bfs_solve(puzzle):
    """Solve the 8-puzzle using BFS and return the sequence of moves."""
    frontier = deque([(puzzle.copy(), [])])  # Queue of (puzzle, moves)
    explored = set()
    explored_nodes = 0

    while frontier:
        current_puzzle, moves = frontier.popleft()

        if current_puzzle.is_solved():
            return moves, explored_nodes  # Return the list of moves to solve the puzzle and explored nodes

        if current_puzzle not in explored:
            explored.add(current_puzzle)
            explored_nodes += 1

            for move in current_puzzle.legal_moves():
                new_puzzle = current_puzzle.result(move)
                frontier.append((new_puzzle, moves + [move]))

    return [], explored_nodes  # No solution found


def print_solution_path(puzzle_initial_state, solution_moves):
    """Print the puzzle states along the solution path."""
    current_puzzle = EightPuzzle(puzzle_initial_state.copy())  # Start from the initial state
    print("Initial state:")
    print(current_puzzle)

    for move in solution_moves:
        current_puzzle.move(move)
        print(f"After move {move}:")
        print(current_puzzle)


# Puzzle Display and Button-based Manual Progression
def update_display(puzzle, ax):
    """Update the puzzle display."""
    ax.clear()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)

    # Reverse row index to show first row at the top
    for i in range(3):
        for j in range(3):
            value = puzzle.state[2 - i][j]  # Reverse row index
            label = '' if value == 0 else str(value)
            ax.text(j + 0.5, i + 0.5, label, ha='center', va='center', fontsize=45, fontweight='bold',
                    bbox=dict(facecolor='lightgray' if value == 0 else 'white', 
                              edgecolor='black', boxstyle='round,pad=0.6', linewidth=2))

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1)  # Adjust to fit the button
    plt.draw()

def on_click(event, puzzle, ax, solution_moves, step_counter):
    """Handle button click to go to the next move."""
    if step_counter[0] < len(solution_moves):
        move = solution_moves[step_counter[0]]
        puzzle.move(move)
        update_display(puzzle, ax)
        step_counter[0] += 1

def manual_animation_with_button(puzzle_initial_state, solution_moves):
    fig, ax = plt.subplots(figsize=(5, 5))

    # Create a button
    ax_next = plt.axes([0.8, 0.02, 0.15, 0.07])  # Position for button
    next_btn = Button(ax_next, 'Next')

    # Initialize the puzzle to the original initial state (resetting it)
    puzzle = EightPuzzle(puzzle_initial_state.copy())  # Reset puzzle to initial state

    # Initialize step counter for manual progression
    step_counter = [0]

    # Button callback
    next_btn.on_clicked(lambda event: on_click(event, puzzle, ax, solution_moves, step_counter))

    # Initial display of the puzzle
    update_display(puzzle, ax)
    plt.show()


# Heuristic: Disjoint Pattern Database
def disjoint_pattern_db_heuristic(puzzle):
    """Use the precomputed disjoint pattern databases to estimate the heuristic."""
    # Create two separate patterns based on the current puzzle state
    pattern1 = np.where(np.isin(puzzle.state, [1, 2, 3, 4]), puzzle.state, 0)
    pattern2 = np.where(np.isin(puzzle.state, [5, 6, 7, 8]), puzzle.state, 0)

    # Hash the pattern and look up the cost in the pattern databases
    pattern1_cost = pattern_db1.get(pattern_hash(pattern1, pattern1), float('inf'))
    pattern2_cost = pattern_db2.get(pattern_hash(pattern2, pattern2), float('inf'))

    # Return the sum of both pattern costs
    return pattern1_cost + pattern2_cost

# Heuristic: Manhattan Distance
def manhattan_distance(puzzle):
    """Calculate the Manhattan distance of the current state."""
    goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                      4: (1, 0), 5: (1, 1), 6: (1, 2),
                      7: (2, 0), 8: (2, 1), 0: (2, 2)}  # Goal state positions
    total_distance = 0

    for i in range(3):
        for j in range(3):
            value = puzzle.state[i][j]
            if value != 0:
                goal_row, goal_col = goal_positions[value]
                total_distance += abs(i - goal_row) + abs(j - goal_col)

    return total_distance

# Linear Conflict Heuristic Function
def manhattan_distance_with_linear_conflict(puzzle):
    """Calculate the Manhattan distance with linear conflict of the current state."""
    goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                      4: (1, 0), 5: (1, 1), 6: (1, 2),
                      7: (2, 0), 8: (2, 1), 0: (2, 2)}  # Goal state positions
    total_distance = 0
    linear_conflict_penalty = 0

    # Calculate Manhattan distance and detect linear conflicts
    for i in range(3):
        for j in range(3):
            value = puzzle.state[i][j]
            if value != 0:
                goal_row, goal_col = goal_positions[value]
                total_distance += abs(i - goal_row) + abs(j - goal_col)

                # Check for linear conflict in the row
                if goal_row == i:  # Tile is in its correct row
                    for col in range(j + 1, 3):
                        other_value = puzzle.state[i][col]
                        if other_value != 0 and goal_positions[other_value][0] == i:
                            # There is a linear conflict if the current tile should be to the right of the other
                            if goal_positions[value][1] > goal_positions[other_value][1]:
                                linear_conflict_penalty += 2  # Add a penalty for the conflict

                # Check for linear conflict in the column
                if goal_col == j:  # Tile is in its correct column
                    for row in range(i + 1, 3):
                        other_value = puzzle.state[row][j]
                        if other_value != 0 and goal_positions[other_value][1] == j:
                            # There is a linear conflict if the current tile should be below the other
                            if goal_positions[value][0] > goal_positions[other_value][0]:
                                linear_conflict_penalty += 2  # Add a penalty for the conflict

    return total_distance + linear_conflict_penalty


def misplaced_tiles(puzzle):
    """Calculate the number of misplaced tiles in the 8-puzzle."""
    goal_state = np.array([[1, 2, 3],
                           [4, 5, 6],
                           [7, 8, 0]])  # Define the goal state
    current_state = puzzle.state  # The current puzzle state

    misplaced_count = 0
    for i in range(3):
        for j in range(3):
            # Count tiles that are not in their goal position (ignore the blank tile)
            if current_state[i][j] != 0 and current_state[i][j] != goal_state[i][j]:
                misplaced_count += 1

    return misplaced_count


# Heuristic: Misplaced Tiles + Manhattan Distance
def manhattan_distance_with_misplaced_tiles(puzzle):
    """Calculate the Manhattan distance combined with the number of misplaced tiles."""
    goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                      4: (1, 0), 5: (1, 1), 6: (1, 2),
                      7: (2, 0), 8: (2, 1), 0: (2, 2)}  # Goal state positions

    total_manhattan_distance = 0
    misplaced_tiles = 0

    for i in range(3):
        for j in range(3):
            value = puzzle.state[i][j]
            if value != 0:  # Ignore the blank tile
                goal_row, goal_col = goal_positions[value]
                total_manhattan_distance += abs(i - goal_row) + abs(j - goal_col)

                # Count misplaced tiles
                if (i, j) != (goal_row, goal_col):
                    misplaced_tiles += 1

    # Combine both heuristics
    return total_manhattan_distance + misplaced_tiles

def tiles_out_of_row_and_column(puzzle):
    """Heuristic that returns the number of tiles out of their correct row and column."""
    goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                      4: (1, 0), 5: (1, 1), 6: (1, 2),
                      7: (2, 0), 8: (2, 1), 0: (2, 2)}  # Goal state positions
    
    out_of_row = 0
    out_of_col = 0

    for i in range(3):
        for j in range(3):
            value = puzzle.state[i][j]
            if value != 0:  # Don't count the blank tile
                goal_row, goal_col = goal_positions[value]
                
                # Check if the tile is out of its correct row
                if i != goal_row:
                    out_of_row += 1

                # Check if the tile is out of its correct column
                if j != goal_col:
                    out_of_col += 1

    return out_of_row + out_of_col  # Total heuristic value



def n_max_swap_heuristic(puzzle):
    """Heuristic that counts the number of tiles out of place, assuming you can swap any tile with the blank."""
    goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                      4: (1, 0), 5: (1, 1), 6: (1, 2),
                      7: (2, 0), 8: (2, 1), 0: (2, 2)}  # Goal state positions

    out_of_place = 0

    for i in range(3):
        for j in range(3):
            value = puzzle.state[i][j]
            if value != 0:  # Don't count the blank tile
                goal_row, goal_col = goal_positions[value]
                
                # If the tile is not in its correct position, count it
                if (i, j) != (goal_row, goal_col):
                    out_of_place += 1

    return out_of_place  # Total heuristic value


# A* Solver
def a_star_solve(puzzle, heuristic):
    """Solve the 8-puzzle using the A* algorithm and return the sequence of moves."""
    frontier = []  # Priority queue (min-heap)
    heapq.heappush(frontier, (heuristic(puzzle), 0, puzzle.copy(), []))  # (priority, cost, puzzle, moves)
    explored = set()
    explored_nodes = 0

    while frontier:
        _, cost, current_puzzle, moves = heapq.heappop(frontier)

        if current_puzzle.is_solved():
            return moves, explored_nodes  # Return the list of moves to solve the puzzle and explored nodes

        if current_puzzle not in explored:
            explored.add(current_puzzle)
            explored_nodes += 1

            for move in current_puzzle.legal_moves():
                new_puzzle = current_puzzle.result(move)
                new_moves = moves + [move]
                new_cost = cost + 1  # Each move has a cost of 1
                priority = new_cost + heuristic(new_puzzle)  # f(n) = g(n) + h(n)
                heapq.heappush(frontier, (priority, new_cost, new_puzzle, new_moves))

    return [], explored_nodes  # No solution found

# Main execution logic
if __name__ == "__main__":
    # A solvable initial state
    initial_state = [[8, 0, 6],[5, 4, 7],[2, 3, 1]]  # The puzzle state

    if is_solvable(initial_state):
        print("The puzzle is solvable")
    else:
        print("The puzzle is not solvable") 
        raise ValueError

    # Create the EightPuzzle instance
    puzzle = EightPuzzle(initial_state)
    print("### A star Algortihm ###")
    print("#### Manhattan Distance ####")
    tracemalloc.start()
    start_time = time.time()
    solution_moves, explored_nodes = a_star_solve(puzzle,manhattan_distance )
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    elapsed_time = end_time - start_time
    print(f"Computation time: {elapsed_time:.4f} seconds")
    print(f"Current memory usage: {current / 10**6:.6f} MB")
    print(f"Peak memory usage: {peak / 10**6:.6f} MB")
    print(f"Number of explored nodes: {explored_nodes}")
    tracemalloc.stop()

    print()

    print("#### Linear Conflict Heuristic Function  ####")
    tracemalloc.start()
    start_time = time.time()
    solution_moves, explored_nodes = a_star_solve(puzzle,manhattan_distance_with_linear_conflict)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    elapsed_time = end_time - start_time
    print(f"Computation time: {elapsed_time:.4f} seconds")
    print(f"Current memory usage: {current / 10**6:.6f} MB")
    print(f"Peak memory usage: {peak / 10**6:.6f} MB")
    print(f"Number of explored nodes: {explored_nodes}")
    tracemalloc.stop()

    print()

    print("#### Disjoint Pattern Database ####")
    tracemalloc.start()
    start_time = time.time()
    solution_moves, explored_nodes = a_star_solve(puzzle,disjoint_pattern_db_heuristic )
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    elapsed_time = end_time - start_time
    print(f"Computation time: {elapsed_time:.4f} seconds")
    print(f"Current memory usage: {current / 10**6:.6f} MB")
    print(f"Peak memory usage: {peak / 10**6:.6f} MB")
    print(f"Number of explored nodes: {explored_nodes}")
    tracemalloc.stop()

    print()


        
    print("#### Misplaced tiles ####")
    tracemalloc.start()
    start_time = time.time()
    solution_moves, explored_nodes = a_star_solve(puzzle,misplaced_tiles)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    elapsed_time = end_time - start_time
    print(f"Computation time: {elapsed_time:.4f} seconds")
    print(f"Current memory usage: {current / 10**6:.6f} MB")
    print(f"Peak memory usage: {peak / 10**6:.6f} MB")
    print(f"Number of explored nodes: {explored_nodes}")
    tracemalloc.stop()

    print()
    
    print("#### UCS  ####")
    ucs_heuristic = lambda puzzle: 0
    tracemalloc.start()
    start_time = time.time()
    solution_moves, explored_nodes = a_star_solve(puzzle,ucs_heuristic)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    elapsed_time = end_time - start_time
    print(f"Computation time: {elapsed_time:.4f} seconds")
    print(f"Current memory usage: {current / 10**6:.6f} MB")
    print(f"Peak memory usage: {peak / 10**6:.6f} MB")
    print(f"Number of explored nodes: {explored_nodes}")
    tracemalloc.stop()

    print()

    print("#### Misplaced Tiles + Manhattan Distance   NOT CONSISTENT ####")
    tracemalloc.start()
    start_time = time.time()
    solution_moves, explored_nodes = a_star_solve(puzzle,manhattan_distance_with_misplaced_tiles)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    elapsed_time = end_time - start_time
    print(f"Computation time: {elapsed_time:.4f} seconds")
    print(f"Current memory usage: {current / 10**6:.6f} MB")
    print(f"Peak memory usage: {peak / 10**6:.6f} MB")
    print(f"Number of explored nodes: {explored_nodes}")
    tracemalloc.stop()

    print()

    # print("#### tiles out of row and column  ####")
    # tracemalloc.start()
    # start_time = time.time()
    # solution_moves, explored_nodes = a_star_solve(puzzle,tiles_out_of_row_and_column)
    # end_time = time.time()
    # current, peak = tracemalloc.get_traced_memory()
    # elapsed_time = end_time - start_time
    # print(f"Computation time: {elapsed_time:.4f} seconds")
    # print(f"Current memory usage: {current / 10**6:.6f} MB")
    # print(f"Peak memory usage: {peak / 10**6:.6f} MB")
    # print(f"Number of explored nodes: {explored_nodes}")
    # tracemalloc.stop()

    # print()

    # print("#### n-Max SWAP ####")
    # tracemalloc.start()
    # start_time = time.time()
    # solution_moves, explored_nodes = a_star_solve(puzzle,tiles_out_of_row_and_column)
    # end_time = time.time()
    # current, peak = tracemalloc.get_traced_memory()
    # elapsed_time = end_time - start_time
    # print(f"Computation time: {elapsed_time:.4f} seconds")
    # print(f"Current memory usage: {current / 10**6:.6f} MB")
    # print(f"Peak memory usage: {peak / 10**6:.6f} MB")
    # print(f"Number of explored nodes: {explored_nodes}")
    # tracemalloc.stop()
    # Print the explored nodes and the final path (solution)
    # if solution_moves:
    #     print(f"Number of explored nodes: {explored_nodes}")
    #     # print(f"Final path (moves): {solution_moves}")
        
    #     # Print the solution path (puzzle states after each move)
    #     # print_solution_path(initial_state, solution_moves)

    #     # # Animate the solution with a button to go to the next state
    #     # manual_animation_with_button(initial_state, solution_moves)
    # else:
    #     print("No solution found or the puzzle is unsolvable.")
