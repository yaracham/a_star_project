import numpy as np

def manhattan_distance(puzzle):
    """Calculate the Manhattan distance of the current state."""
    goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 0: (2, 2)  # 0 represents the blank tile
    }
    
    total_distance = 0
    for i in range(3):
        for j in range(3):
            value = puzzle.state[i][j].item()
            if value != 0:
                goal_row, goal_col = goal_positions[value]
                total_distance += abs(i - goal_row) + abs(j - goal_col)

    return total_distance

def misplaced_tiles(puzzle):
    """Calculate the number of misplaced tiles."""
    goal_state = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ])
    misplaced_count = np.sum(
        (puzzle.state != goal_state) & (puzzle.state != 0)
    )
    return misplaced_count


def linear_conflict(puzzle):
    goal_state = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ])
    goal_positions = {value: (row, col) for row, row_values in enumerate(goal_state) 
                      for col, value in enumerate(row_values)}
    """Calculate linear conflicts for rows and columns."""
    conflict = 0
    state = puzzle.state
    for row in range(3):
        for col in range(3):
            value = state[row][col]
            if value != 0:
                goal_row, goal_col = goal_positions[value]
                # Check for row conflicts
                if row == goal_row:  # In the same row
                    for k in range(col + 1, 3):
                        if state[goal_row][k] != 0 and goal_positions[state[goal_row][k]][0] == goal_row:
                            conflict += 1
                # Check for column conflicts
                if col == goal_col:  # In the same column
                    for k in range(row + 1, 3):
                        if state[k][goal_col] != 0 and goal_positions[state[k][goal_col]][1] == goal_col:
                            conflict += 1
    return conflict

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


def manhattan_distance_with_misplaced_tiles(puzzle):
    return (manhattan_distance(puzzle)+misplaced_tiles(puzzle))


def tiles_out_of_row_and_column(puzzle):
    """Calculate the number of tiles out of their correct row and column."""
    total = 0

    # Check for tiles out of correct row
    for i in range(3):
        for j in range(3):
            tile = puzzle.state[i][j]
            if tile != 0 and (tile - 1) // 3 != i:
                total += 1

    # Check for tiles out of correct column
    for i in range(3):
        for j in range(3):
            tile = puzzle.state[i][j]
            if tile != 0 and (tile - 1) % 3 != j:
                total += 1

    return total

def manhattan_misplaced_linear(state):
    return (manhattan_distance(state) + 
            misplaced_tiles(state) + 
            linear_conflict(state))