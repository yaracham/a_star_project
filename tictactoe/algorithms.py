from actions import *
from random import randint
from heuristics import HEURISTIC
import time

pruningMax = 0
pruningMin = 0
cutOffOccured = False

inf = 9999999999
neg_inf = -9999999999

def RANDOM_PLAY(state):
    state.children = ACTIONS(state)
    retVal = randint(0, len(state.children) - 1)
    return state.children[retVal]

def ALPHA_BETA_SEARCH(state, start):
    # Start alpha-beta search with initial alpha (-inf) and beta (inf)
    v = MAX_VALUE(state=state, alpha=neg_inf, beta=inf, start=start)
    # Choose the move corresponding to the best value found
    retVal = list(filter(lambda x: x.value == v, state.children))[0]
    return retVal

def MAX_VALUE(state, alpha, beta, start):
    global cutOffOccured
    global pruningMax
    global pruningMin

    # Check if the state is terminal
    if TERMINAL_TEST(state=state):
        return UTILITY(state=state)

    # Check if the search time has exceeded the 10-second limit
    duration = time.time() - start
    if duration >= 10:
        cutOffOccured = True
        return HEURISTIC(state)  # Return heuristic value if time limit exceeded

    v = neg_inf
    new_alpha = alpha
    state.children = ACTIONS(state)  # Generate children for the state

    for a in state.children:
        v = max(v, MIN_VALUE(state=a, alpha=new_alpha, beta=beta, start=start))
        a.value = v  # Store value in the current child state

        # Check for pruning
        if v >= beta:
            pruningMax += 1  # Increment pruning count for Max-Value
            return v
        new_alpha = max(new_alpha, v)  # Update alpha

    return v

def MIN_VALUE(state, alpha, beta, start):
    global cutOffOccured
    global pruningMax
    global pruningMin

    # Check if the state is terminal
    if TERMINAL_TEST(state=state):
        return UTILITY(state=state)

    # Check if the search time has exceeded the 10-second limit
    duration = time.time() - start
    if duration >= 10:
        cutOffOccured = True
        return HEURISTIC(state)  # Return heuristic value if time limit exceeded

    v = inf
    new_beta = beta
    state.children = ACTIONS(state)  # Generate children for the state

    for a in state.children:
        v = min(v, MAX_VALUE(state=a, alpha=alpha, beta=new_beta, start=start))
        a.value = v  # Store value in the current child state

        # Check for pruning
        if v <= alpha:
            pruningMin += 1  # Increment pruning count for Min-Value
            return v
        new_beta = min(new_beta, v)  # Update beta

    return v
