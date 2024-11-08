from actions import *

def evaluation_function(state, depth, max_depth=5):
    if depth >= max_depth:
        return heuristic_score(state)
    
    if TERMINAL_TEST(state):  # If the state is a win/lose/draw
        return UTILITY(state)

    return heuristic_score(state)

def heuristic_score(state):
    score = 0
    winning_lines = [
        # Rows
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(3, 0), (3, 1), (3, 2), (3, 3)],
        # Columns
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(0, 3), (1, 3), (2, 3), (3, 3)],
        # Diagonals
        [(0, 0), (1, 1), (2, 2), (3, 3)],
        [(0, 3), (1, 2), (2, 1), (3, 0)]
    ]
    
    for line in winning_lines:
        x_count = sum(1 for (i, j) in line if state.table[i, j] == x_player)
        o_count = sum(1 for (i, j) in line if state.table[i, j] == o_player)

        # Award points based on counts in each line, prefer complete rows/columns/diagonals
        if x_count > 0 and o_count == 0:
            score += x_count**2  # Higher score for more x's in a row
        elif o_count > 0 and x_count == 0:
            score -= o_count**2  # Lower score for more o's in a row

    return score
