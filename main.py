import time
import tracemalloc
import pickle
import matplotlib.pyplot as plt

from solvers import *
from eight_puzzle import EightPuzzle
from display_utils import *
from loaded_states import states

from heuristics import *




# Function to load puzzles from a file
def load_puzzles_from_file(filename="puzzles.pkl"):
    with open(filename, "rb") as f:
        puzzles = pickle.load(f)
    return puzzles

# Function to calculate the average execution time and explored nodes
def test_heuristics_on_multiple_cases(num_tests, heuristics):
    avg_execution_times = {h[0]: 0 for h in heuristics}
    avg_explored_nodes = {h[0]: 0 for h in heuristics}

    for _ in range(num_tests):
        # Generate a random solvable puzzle
        puzzles = load_puzzles_from_file()
        puzzle = EightPuzzle(puzzles)

        for h in heuristics:
            heuristic_name, heuristic = h

            # Start memory and time tracking
            tracemalloc.start()
            start_time = time.time()

            # Solve the puzzle with the current heuristic
            solution_moves, explored_nodes = a_star_solve(puzzle, heuristic)

            # End time tracking
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()

            # Stop memory tracking
            tracemalloc.stop()

            # Calculate elapsed time
            elapsed_time = end_time - start_time

            # Accumulate the times and explored nodes
            avg_execution_times[heuristic_name] += elapsed_time
            avg_explored_nodes[heuristic_name] += explored_nodes

    # Compute the averages
    avg_execution_times = {h: time / num_tests for h, time in avg_execution_times.items()}
    avg_explored_nodes = {h: nodes / num_tests for h, nodes in avg_explored_nodes.items()}

    return avg_execution_times, avg_explored_nodes

# Main function to run the heuristics on 1000 random cases
if __name__ == "__main__":
    # A solvable initial state
    initial_state = [[8, 0, 6],[5, 4, 7],[2, 3, 1]]  # The puzzle state

    if is_solvable(initial_state):
        print("The puzzle is solvable")
    else:
        print("The puzzle is not solvable") 
        raise ValueError

        # Define all the heuristics to test
    heuristics = [
        ("Manhattan Distance", manhattan_distance),
        # ("Linear Conflict", linear_conflict),
        # ("Misplaced Tiles", misplaced_tiles),
        ("Manhattan Distance + Misplaced Tiles",manhattan_distance_with_misplaced_tiles),
        ("Manhattan Distance + Linear Conflict",manhattan_distance_with_linear_conflict)
        # ("Manhattan Distance + Linear conflict + Misplaced Tiles ",manhattan_misplaced_linear),
        # ("Tiles Out of Row and Column", tiles_out_of_row_and_column),
        # ("N Max Swap", n_max_swap_heuristic),
        # ("Uniform Cost Search", lambda p: 0)
    ]
    # Create the EightPuzzle instance
    puzzle = EightPuzzle(initial_state)
    print("### A star Algorithm ###")
    for h in heuristics:
        print(h[0])
        tracemalloc.start()
        start_time = time.time()
        solution_moves, explored_nodes = a_star_solve(puzzle,h[1] )
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        elapsed_time = end_time - start_time
        print(f"Computation time: {elapsed_time:.4f} seconds")
        print(f"Current memory usage: {current / 10**6:.6f} MB")
        print(f"Peak memory usage: {peak / 10**6:.6f} MB")
        print(f"Number of explored nodes: {explored_nodes}")
        tracemalloc.stop()

        print()

    num_tests = len(states)  # The number of puzzles you loaded

    # Initialize accumulators for performance metrics
    avg_execution_times = {h[0]: 0 for h in heuristics}
    avg_explored_nodes = {h[0]: 0 for h in heuristics}

    print("### A* Algorithm Performance on Pre-Generated Cases ###")
    for puzzle_state in states:
        puzzle = EightPuzzle(puzzle_state)

        for h in heuristics:
            print(h[0])
            heuristic_name, heuristic = h

            # Start memory and time tracking
            tracemalloc.start()
            start_time = time.time()

            # Solve the puzzle with the current heuristic
            solution_moves, explored_nodes = a_star_solve(puzzle, heuristic)

            # End time tracking
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()

            # Stop memory tracking
            tracemalloc.stop()

            # Calculate elapsed time
            elapsed_time = end_time - start_time

            # Accumulate the times and explored nodes
            avg_execution_times[heuristic_name] += elapsed_time
            avg_explored_nodes[heuristic_name] += explored_nodes
            print("done")
    # Compute the averages
    avg_execution_times = {h: time / num_tests for h, time in avg_execution_times.items()}
    avg_explored_nodes = {h: nodes / num_tests for h, nodes in avg_explored_nodes.items()}

    # Display the results
    for heuristic_name in avg_execution_times:
        print(f"#### {heuristic_name} ####")
        print(f"Average computation time: {avg_execution_times[heuristic_name]:.4f} seconds")
        print(f"Average explored nodes: {avg_explored_nodes[heuristic_name]:.2f}")
        print()

    # Plot the data
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Plot average execution time
    ax[0].bar(avg_execution_times.keys(), avg_execution_times.values(), color='blue')
    ax[0].set_title('Average Execution Time (seconds)')
    ax[0].set_ylabel('Time (s)')
    ax[0].tick_params(axis='x', rotation=45)

    # Plot average explored nodes
    ax[1].bar(avg_explored_nodes.keys(), avg_explored_nodes.values(), color='red')
    ax[1].set_title('Average Explored Nodes')
    ax[1].set_ylabel('Number of Nodes')
    ax[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()