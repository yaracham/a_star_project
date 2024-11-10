from state import *
from copy import deepcopy
from state import x_player, o_player

computer_player = x_player
human_player = o_player

min_util = -1000
max_util = +1000

def other_player(player):
    if player == x_player:
        return o_player
    else:
        return x_player
    

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

                stats.maxDepthReached = max(stats.maxDepthReached, childState.depth)

                children.append(childState)

    stats.totalNodes += len(children)
    return children


def PLAYER_UTIL(player):
    if player == computer_player:
        return max_util
    elif player == human_player:
        return min_util
    return 0

def TERMINAL_TEST(state):
    player = other_player(player=state.nextPlayer)
    if state.table[0, 0] == state.table[0, 1] \
            and state.table[0, 1] == state.table[0, 2] \
            and state.table[0, 2] == state.table[0, 3] \
            and state.table[0, 0] != empty:
        return (True,PLAYER_UTIL(state.table[0, 0]))
    if state.table[1, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[1, 2] \
            and state.table[1, 2] == state.table[1, 3] \
            and state.table[1, 0] != empty:
        return (True,PLAYER_UTIL(state.table[1, 0]))    
    if state.table[2, 0] == state.table[2, 1] \
            and state.table[2, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[2, 3] \
            and state.table[2, 0] != empty:
        return (True,PLAYER_UTIL(state.table[2, 0]))    
    if state.table[3, 0] == state.table[3, 1] \
            and state.table[3, 1] == state.table[3, 2] \
            and state.table[3, 2] == state.table[3, 3] \
            and state.table[3, 0] != empty:
        return (True,PLAYER_UTIL(state.table[3, 0]))    
    if state.table[0, 0] == state.table[1, 0] \
            and state.table[1, 0] == state.table[2, 0] \
            and state.table[2, 0] == state.table[3, 0] \
            and state.table[0, 0] != empty:
        return (True,PLAYER_UTIL(state.table[0, 0]))    
    if state.table[0, 1] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 1] \
            and state.table[0, 1] != empty:
        return (True,PLAYER_UTIL(state.table[0, 1]))    
    if state.table[0, 2] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 2] \
            and state.table[0, 2] != empty:
        return (True,PLAYER_UTIL(state.table[0, 2]))    
    if state.table[0, 3] == state.table[1, 3] \
            and state.table[1, 3] == state.table[2, 3] \
            and state.table[2, 3] == state.table[3, 3] \
            and state.table[0, 3] != empty:
        return (True,PLAYER_UTIL(state.table[0, 3]))    
    if state.table[0, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 3] \
            and state.table[0, 0] != empty:
        return (True,PLAYER_UTIL(state.table[0, 0]))    
    if state.table[0, 3] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 0] \
            and state.table[0, 3] != empty:
        return (True,PLAYER_UTIL(state.table[0, 3]))
    if state.is_full():
        return (True,0)
    return (False,-1)


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
    
    if player_count == 3 and empty_count == 1:
        score += 10 
    
    if opponent_count == 3 and empty_count == 1:
        score -= 10  
    
    return score


def evaluation_function(state):
    """
    Evaluation function for non-terminal states that computes the heuristic score.
    - Positive score for potential lines of four for the player.
    - Negative score for opponent's threats (potential lines of four).
    """
    score = 0
    board = state.table

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

    for line in lines:
        score += evaluate_line_for_four(line)
    
    return score

def evaluation_function_2(state):
    x3 = 0
    x2 = 0
    x1 = 0
    o3 = 0
    o2 = 0
    o1 = 0

    # check row wise
    for r in range(0, size):
        os = 0
        xs = 0
        for c in range(0, size):
            if state.table[r, c] == x_player:
                xs += 1
            elif state.table[r, c] == o_player:
                os += 1

        if xs == 0:
            if os == 1:
                o1 += 1
            elif os == 2:
                o2 += 1
            elif os == 3:
                o3 += 1

        if os == 0:
            if xs == 1:
                x1 += 1
            elif xs == 2:
                x2 += 1
            elif xs == 3:
                x3 += 1

    # check column wise
    for c in range(0, size):
        os = 0
        xs = 0
        for r in range(0, size):
            if state.table[r, c] == x_player:
                xs += 1
            elif state.table[r, c] == o_player:
                os += 1

        if xs == 0:
            if os == 1:
                o1 += 1
            elif os == 2:
                o2 += 1
            elif os == 3:
                o3 += 1

        if os == 0:
            if xs == 1:
                x1 += 1
            elif xs == 2:
                x2 += 1
            elif xs == 3:
                x3 += 1

    # check main diagonal
    os = 0
    xs = 0
    for i in range(0, size):
        if state.table[i, i] == x_player:
            xs += 1
        elif state.table[i, i] == o_player:
            os += 1

    if xs == 0:
        if os == 1:
            o1 += 1
        elif os == 2:
            o2 += 1
        elif os == 3:
            o3 += 1

    if os == 0:
        if xs == 1:
            x1 += 1
        elif xs == 2:
            x2 += 1
        elif xs == 3:
            x3 += 1

    # check main diagonal
    os = 0
    xs = 0
    for i in range(0, size):
        if state.table[size - i - 1, i] == x_player:
            xs += 1
        elif state.table[size - i - 1, i] == o_player:
            os += 1

    if xs == 0:
        if os == 1:
            o1 += 1
        elif os == 2:
            o2 += 1
        elif os == 3:
            o3 += 1

    if os == 0:
        if xs == 1:
            x1 += 1
        elif xs == 2:
            x2 += 1
        elif xs == 3:
            x3 += 1

    return (6 * x3 + 3 * x2 + x1) - (6 * o3 + 3 * o2 + o1) - 0.3*(state.depth)
