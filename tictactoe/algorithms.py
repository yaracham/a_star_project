from actions import *
from random import randint
from heuristics import HEURISTIC
import time

inf = 9999999999
neg_inf = -9999999999


def ALPHA_BETA_SEARCH(state, start, stats):
    v = MAX_VALUE(state=state, alpha=neg_inf, beta=inf, start=start, stats=stats)
    retVal = list(filter(lambda x: x.value == v, state.children))[0]
    return retVal

def MAX_VALUE(state, alpha, beta, start, stats):
    # Update the maximum depth reached
    stats.maxDepthReached = max(stats.maxDepthReached, state.depth)

    # Increment the total nodes explored
    stats.totalNodes += 1
 
    # Check if the state is terminal
    if TERMINAL_TEST(state=state):
        return UTILITY(state=state)

        #Check if reached maxDepth
    if state.depth == stats.maxDepth:
        return evaluation_function(state= state)
    
    # Check if the search time has exceeded the 10-second limit
    duration = time.time() - start
    if duration >= 10:
        stats.cutOffOccured = True
        return HEURISTIC(state)  # Return heuristic value if time limit exceeded

    v = neg_inf
    state.children = ACTIONS(state,stats)  # Generate children for the state

    for a in state.children:
        v = max(v, MIN_VALUE(state=a, alpha=alpha, beta=beta, start=start, stats=stats))
        a.value = v  # Store value in the current child state

        # Check for pruning
        if v >= beta:
            stats.pruningMax += 1  # Increment pruning count for Max-Value
            return v
        alpha = max(alpha, v)  # Update alpha

    return v

def MIN_VALUE(state, alpha, beta, start, stats):
    # Update the maximum depth reached
    stats.maxDepthReached = max(stats.maxDepthReached, state.depth)

    # Increment the total nodes explored
    stats.totalNodes += 1
    
    # Check if the state is terminal
    if TERMINAL_TEST(state=state):
        return UTILITY(state=state)

        #Check if reached maxDepth
    if state.depth == stats.maxDepth:
        return evaluation_function(state= state)
    
    # Check if the search time has exceeded the 10-second limit
    duration = time.time() - start
    if duration >= 10:
        stats.cutOffOccured = True
        return HEURISTIC(state)  # Return heuristic value if time limit exceeded

    v = inf
    state.children = ACTIONS(state,stats)  # Generate children for the state

    for a in state.children:
        v = min(v, MAX_VALUE(state=a, alpha=alpha, beta=beta, start=start, stats=stats))
        a.value = v  # Store value in the current child state

        # Check for pruning
        if v <= alpha:
            stats.pruningMin += 1  # Increment pruning count for Min-Value
            return v
        beta = min(beta, v)  # Update beta

    return v
