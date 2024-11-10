from utilities import *
import time

inf = 9999999999
neg_inf = -9999999999

#without pruning 

def alpha_beta_search_no_pruning(state, start, stats):
    v = max_no_pruning(state=state,start=start, depth=0, stats=stats)
    retVal = list(filter(lambda x: x.value == v, state.children))[0]
    return retVal

def max_no_pruning(state, start, depth, stats):
    if depth > stats.maxDepth:
        return evaluation_function_2(state= state)
    stats.maxDepthReached = max(stats.maxDepthReached, depth)
    stats.totalNodes += 1
 
    print("depth in MAx ============================",depth)

    if TERMINAL_TEST(state=state)[0]:
        return TERMINAL_TEST(state=state)[1]

    duration = time.time() - start
    if duration >= 10:
        stats.cutOffOccured = True
        return evaluation_function_2(state)  

    v = neg_inf
    state.children = ACTIONS(state,stats)  

    for a in state.children:
        v = max(v, min_no_pruning(state=a, start=start, depth=depth+1, stats=stats))
        a.value = v   

    return v

def min_no_pruning(state, start, depth, stats):
    if depth > stats.maxDepth:
        return evaluation_function_2(state= state)
    
    stats.maxDepthReached = max(stats.maxDepthReached, depth)
    stats.totalNodes += 1

    print("depth in MIN ============================",depth)

    if TERMINAL_TEST(state=state)[0]:
        return TERMINAL_TEST(state=state)[1]

    duration = time.time() - start
    if duration >= 10:
        stats.cutOffOccured = True
        return evaluation_function_2(state)  

    v = inf
    state.children = ACTIONS(state,stats) 

    for a in state.children:
        v = min(v, max_no_pruning(state=a, start=start, depth=depth+1, stats=stats))
        a.value = v   

    return v




#with pruning

def alpha_beta_search_pruning(state, start, stats):
    v = max_pruning(state=state, alpha=neg_inf, beta=inf, start=start, depth=0, stats=stats)
    retVal = list(filter(lambda x: x.value == v, state.children))[0]
    return retVal

def max_pruning(state, alpha, beta, start, depth, stats):
    if depth > stats.maxDepth:
        return evaluation_function_2(state= state)
    stats.maxDepthReached = max(stats.maxDepthReached, depth)
    stats.totalNodes += 1
 
    print("depth in MAx ============================",depth)

    if TERMINAL_TEST(state=state)[0]:
        return TERMINAL_TEST(state=state)[1]

    duration = time.time() - start
    if duration >= 10:
        stats.cutOffOccured = True
        return evaluation_function_2(state)  

    v = neg_inf
    state.children = ACTIONS(state,stats)  

    for a in state.children:
        v = max(v, min_pruning(state=a, alpha=alpha, beta=beta, start=start, depth=depth+1, stats=stats))
        a.value = v  

        if v >= beta:
            stats.pruningMax += 1  
            return v
        alpha = max(alpha, v)  

    return v

def min_pruning(state, alpha, beta, start, depth, stats):
    if depth > stats.maxDepth:
        return evaluation_function_2(state= state)
    
    stats.maxDepthReached = max(stats.maxDepthReached, depth)
    stats.totalNodes += 1

    print("depth in MIN ============================",depth)

    if TERMINAL_TEST(state=state)[0]:
        return TERMINAL_TEST(state=state)[1]

    duration = time.time() - start
    if duration >= 10:
        stats.cutOffOccured = True
        return evaluation_function_2(state)  

    v = inf
    state.children = ACTIONS(state,stats) 

    for a in state.children:
        v = min(v, max_pruning(state=a, alpha=alpha, beta=beta, start=start, depth=depth+1, stats=stats))
        a.value = v  

        if v <= alpha:
            stats.pruningMin += 1 
            return v
        beta = min(beta, v)  

    return v
