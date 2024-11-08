from state import *
from utils import *
from copy import deepcopy

def ACTIONS(state, stats, size=4):
    children = []
    for i in range(size):
        for j in range(size):
            if state.table[i, j] == empty:
                childTable = deepcopy(state.table)
                childTable[i, j] = state.nextPlayer
                childState = State(nextPlayer=state.nextPlayer)
                childState.nextPlayer = other_player(state.nextPlayer)
                childState.table = childTable
                childState.value = state.value
                childState.depth = state.depth + 1

                # Update max depth reached
                stats.maxDepthReached = max(stats.maxDepthReached, childState.depth)

                children.append(childState)

    # Update total nodes generated
    stats.totalNodes += len(children)
    return children


def TERMINAL_TEST(state):
    if state.is_full():
        return True

    player = other_player(player=state.nextPlayer)
    if state.table[0, 0] == state.table[0, 1] \
            and state.table[0, 1] == state.table[0, 2] \
            and state.table[0, 2] == state.table[0, 3] \
            and state.table[0, 0] != empty:
        return True
    if state.table[1, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[1, 2] \
            and state.table[1, 2] == state.table[1, 3] \
            and state.table[1, 0] != empty:
        return True
    if state.table[2, 0] == state.table[2, 1] \
            and state.table[2, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[2, 3] \
            and state.table[2, 0] != empty:
        return True
    if state.table[3, 0] == state.table[3, 1] \
            and state.table[3, 1] == state.table[3, 2] \
            and state.table[3, 2] == state.table[3, 3] \
            and state.table[3, 0] != empty:
        return True
    if state.table[0, 0] == state.table[1, 0] \
            and state.table[1, 0] == state.table[2, 0] \
            and state.table[2, 0] == state.table[3, 0] \
            and state.table[0, 0] != empty:
        return True
    if state.table[0, 1] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 1] \
            and state.table[0, 1] != empty:
        return True
    if state.table[0, 2] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 2] \
            and state.table[0, 2] != empty:
        return True
    if state.table[0, 3] == state.table[1, 3] \
            and state.table[1, 3] == state.table[2, 3] \
            and state.table[2, 3] == state.table[3, 3] \
            and state.table[0, 3] != empty:
        return True
    if state.table[0, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 3] \
            and state.table[0, 0] != empty:
        return True
    if state.table[0, 3] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 0] \
            and state.table[0, 3] != empty:
        return True

    return False

def UTILITY(state):
    if state.table[0, 0] == state.table[0, 1] \
            and state.table[0, 1] == state.table[0, 2] \
            and state.table[0, 2] == state.table[0, 3] \
            and state.table[0, 0] != empty:
        return PLAYER_UTIL(state.table[0, 0])
    if state.table[1, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[1, 2] \
            and state.table[1, 2] == state.table[1, 3] \
            and state.table[1, 0] != empty:
        return PLAYER_UTIL(state.table[1, 0])
    if state.table[2, 0] == state.table[2, 1] \
            and state.table[2, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[2, 3] \
            and state.table[2, 0] != empty:
        return PLAYER_UTIL(state.table[2, 0])
    if state.table[3, 0] == state.table[3, 1] \
            and state.table[3, 1] == state.table[3, 2] \
            and state.table[3, 2] == state.table[3, 3] \
            and state.table[3, 0] != empty:
        return PLAYER_UTIL(state.table[3, 0])
    if state.table[0, 0] == state.table[1, 0] \
            and state.table[1, 0] == state.table[2, 0] \
            and state.table[2, 0] == state.table[3, 0] \
            and state.table[0, 0] != empty:
        return PLAYER_UTIL(state.table[0, 0])
    if state.table[0, 1] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 1] \
            and state.table[0, 1] != empty:
        return PLAYER_UTIL(state.table[0, 1])
    if state.table[0, 2] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 2] \
            and state.table[0, 2] != empty:
        return PLAYER_UTIL(state.table[0, 2])
    if state.table[0, 3] == state.table[1, 3] \
            and state.table[1, 3] == state.table[2, 3] \
            and state.table[2, 3] == state.table[3, 3] \
            and state.table[0, 3] != empty:
        return PLAYER_UTIL(state.table[0, 3])
    if state.table[0, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 3] \
            and state.table[0, 0] != empty:
        return PLAYER_UTIL(state.table[0, 0])
    if state.table[0, 3] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 0] \
            and state.table[0, 3] != empty:
        return PLAYER_UTIL(state.table[0, 3])

    return 0

def evaluate_line_for_four(cells):
    """
    Helper function to evaluate a single line (row, column, or diagonal)
    Returns a score based on the number of potential lines of four.
    A potential line of four is when a player has 3 marks and 1 empty cell.
    """
    player_count = sum(1 for cell in cells if cell == 'X')
    opponent_count = sum(1 for cell in cells if cell == 'O')
    empty_count = sum(1 for cell in cells if cell is None)

    score = 0
    
    # Check if the player has 3 marks and 1 empty space
    if player_count == 3 and empty_count == 1:
        score += 10  # Potential line of four for the player
    
    # Check if the opponent has 3 marks and 1 empty space (threat)
    if opponent_count == 3 and empty_count == 1:
        score -= 10  # Block the opponent's potential line of four
    
    return score


def evaluation_function(state):
    """
    Evaluation function for non-terminal states that computes the heuristic score.
    - Positive score for potential lines of four for the player.
    - Negative score for opponent's threats (potential lines of four).
    """
    score = 0
    board = state.table

    # Evaluate each of the lines (rows, columns, diagonals)
    lines = [
        # Rows
        [board[0, 0], board[0, 1], board[0, 2], board[0, 3]],
        [board[1, 0], board[1, 1], board[1, 2], board[1, 3]],
        [board[2, 0], board[2, 1], board[2, 2], board[2, 3]],
        [board[3, 0], board[3, 1], board[3, 2], board[3, 3]],
        
        # Columns
        [board[0, 0], board[1, 0], board[2, 0], board[3, 0]],
        [board[0, 1], board[1, 1], board[2, 1], board[3, 1]],
        [board[0, 2], board[1, 2], board[2, 2], board[3, 2]],
        [board[0, 3], board[1, 3], board[2, 3], board[3, 3]],
        
        # Diagonals
        [board[0, 0], board[1, 1], board[2, 2], board[3, 3]],
        [board[0, 3], board[1, 2], board[2, 1], board[3, 0]]
    ]

    # Sum the score from each line
    for line in lines:
        score += evaluate_line_for_four(line)
    
    return score
