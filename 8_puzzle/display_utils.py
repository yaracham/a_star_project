import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from eight_puzzle import EightPuzzle 

def is_solvable(puzzle):
    """Check if the puzzle is solvable by counting inversions."""
    flattened_puzzle = [tile for row in puzzle for tile in row if tile != 0]
    inversions = sum(1 for i in range(len(flattened_puzzle)) for j in range(i + 1, len(flattened_puzzle)) if flattened_puzzle[i] > flattened_puzzle[j])
    return inversions % 2 == 0

def print_solution_path(puzzle_initial_state, solution_moves):
    """Print the puzzle states along the solution path."""
    current_puzzle = EightPuzzle(puzzle_initial_state.copy()) 
    print("Initial state:")
    print(current_puzzle)

    for move in solution_moves:
        current_puzzle.move(move)
        print(f"After move {move}:")
        print(current_puzzle)

def update_display(puzzle, ax):
    """Update the puzzle display for animation."""
    ax.clear()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)


    for i in range(3):
        for j in range(3):
            value = puzzle.state[2 - i][j] 
            label = '' if value == 0 else str(value)
            ax.text(j + 0.5, i + 0.5, label, ha='center', va='center', fontsize=45, fontweight='bold',
                    bbox=dict(facecolor='lightgray' if value == 0 else 'white',
                              edgecolor='black', boxstyle='round,pad=0.6', linewidth=2))

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1)  
    plt.draw()

def on_click(event, puzzle, ax, solution_moves, step_counter):
    """Handle button click to go to the next move."""
    if step_counter[0] < len(solution_moves):
        move = solution_moves[step_counter[0]]
        puzzle.move(move)
        update_display(puzzle, ax)
        step_counter[0] += 1

def manual_animation_with_button(puzzle_initial_state, solution_moves):
    """Manually progress through the solution with a button."""
    fig, ax = plt.subplots(figsize=(5, 5))


    ax_next = plt.axes([0.8, 0.02, 0.15, 0.07])  
    next_btn = Button(ax_next, 'Next')

    puzzle = EightPuzzle(puzzle_initial_state.copy())  

    step_counter = [0]

    next_btn.on_clicked(lambda event: on_click(event, puzzle, ax, solution_moves, step_counter))

    update_display(puzzle, ax)
    plt.show()
