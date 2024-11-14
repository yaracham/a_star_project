from utilities import *
import time
from random import randint

inf = 9999999999
neg_inf = -9999999999

#without pruning 

def minimax_no_pruning(state, start, stats, level):
    v = max_no_pruning(state=state, start=start, depth=0, stats=stats,level=level)
    retVal = list(filter(lambda x: x.value == v, state.children))[0]
    print("CHOSEN STATE utility:", v)
    retVal.printBoard()
    return retVal

def max_no_pruning(state, start, depth, stats, level):
    print()
    if depth >= stats.maxDepth:
        print("MAX DEPTH REACHED, utility = ",evluation_function(state= state, level=level))
        state.printBoard()
        print()
        return evluation_function(state= state, level=level)
    
    stats.maxDepthReached = max(stats.maxDepthReached, depth)
    stats.totalNodes += 1

    terminal = TERMINAL_TEST(state=state)
    if terminal[0]:
        print("TERMINAL STATE: ", terminal[1])
        state.printBoard()
        print()
        return terminal[1]

    duration = time.time() - start
    if duration >= 10:
        stats.cutOffOccured = True
        return evluation_function(state= state, level=level)

    v = neg_inf
    state.children = ACTIONS(state,stats)  

    for a in state.children:
        v = max(v, min_no_pruning(state=a, start=start, depth=depth+1, stats=stats, level=level))
        a.value = v   

    return v

def min_no_pruning(state, start, depth, stats, level):
    print()
    if depth >= stats.maxDepth:
        print("MAX DEPTH REACHED, utility = ",evluation_function(state= state, level=level) )
        state.printBoard()
        print()
        return evluation_function(state= state, level=level)
    
    stats.maxDepthReached = max(stats.maxDepthReached, depth)
    stats.totalNodes += 1

    terminal = TERMINAL_TEST(state=state)
    if terminal[0]:
        print("TERMINAL STATE: ", terminal[1])
        state.printBoard()
        print()
        return terminal[1]

    duration = time.time() - start
    if duration >= 10:
        stats.cutOffOccured = True
        return evluation_function(state= state, level=level) 

    v = inf
    state.children = ACTIONS(state,stats) 

    for a in state.children:
        v = min(v, max_no_pruning(state=a, start=start, depth=depth+1, stats=stats, level=level))
        a.value = v   

    return v




#with pruning

def alpha_beta_search_pruning(state, start, stats, level):
    v = max_pruning(state=state, alpha=neg_inf, beta=inf, start=start, depth=0, stats=stats,level=level)
    retVal = list(filter(lambda x: x.value == v, state.children))[0]
    print("CHOSEN STATE utility:", v)
    retVal.printBoard()
    return retVal

def max_pruning(state, alpha, beta, start, depth, stats, level):
    print()
    if depth >= stats.maxDepth:
        print("MAX DEPTH REACHED, utility = ",evluation_function(state= state, level=level))
        state.printBoard()
        print()
        return evluation_function(state= state, level=level)
    
    stats.maxDepthReached = max(stats.maxDepthReached, depth)
    stats.totalNodes += 1

    terminal = TERMINAL_TEST(state=state)
    if terminal[0]:
        print("TERMINAL STATE: ", terminal[1])
        state.printBoard()
        print()
        return terminal[1]

    v = neg_inf
    state.children = ACTIONS(state,stats)  

    for a in state.children:
        v = max(v, min_pruning(state=a, alpha=alpha, beta=beta, start=start, depth=depth+1, stats=stats, level=level))
        a.value = v  

        if v >= beta:
            stats.pruningMax += 1  
            return v
        alpha = max(alpha, v)  

    return v

def min_pruning(state, alpha, beta, start, depth, stats, level):
    print()
    if depth >= stats.maxDepth:
        print("MAX DEPTH REACHED, utility = ",evluation_function(state= state, level=level) )
        state.printBoard()
        print()
        return evluation_function(state= state, level=level)
    
    stats.maxDepthReached = max(stats.maxDepthReached, depth)
    stats.totalNodes += 1

    terminal = TERMINAL_TEST(state=state)
    if terminal[0]:
        print("TERMINAL STATE: ", terminal[1])
        state.printBoard()
        print()
        return terminal[1]

    v = inf
    state.children = ACTIONS(state,stats) 

    for a in state.children:
        v = min(v, max_pruning(state=a, alpha=alpha, beta=beta, start=start, depth=depth+1, stats=stats, level=level))
        a.value = v  

        if v <= alpha:
            stats.pruningMin += 1 
            return v
        beta = min(beta, v)  

    return v


