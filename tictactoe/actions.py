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