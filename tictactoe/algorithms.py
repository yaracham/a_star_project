from actions import *
from easyLevel import *

inf = 9999999999
neg_inf = -9999999999

def ALPHA_BETA_SEARCH(state, stats, evaluation_function=None, max_depth=5):
    # Default evaluation function if none is provided
    if evaluation_function is None:
        evaluation_function = heuristic_score  # Ensure you have a default function like `heuristic_score`

    # Start the alpha-beta search with initial alpha (-inf) and beta (inf)
    best_move = None
    best_value = -float('inf')
    
    # Initialize children of the current state
    state.children = ACTIONS(state, stats)  # Generate possible moves (children) based on the current state
    
    # Perform alpha-beta search to find the best value
    def MAX_VALUE(state, alpha, beta, depth):
        nonlocal best_move, best_value
        if depth >= max_depth or TERMINAL_TEST(state):
            return evaluation_function(state)
        
        value = -float('inf')
        for child in state.children:
            # Call MIN_VALUE for the next level (minimizing player)
            value = max(value, MIN_VALUE(child, alpha, beta, depth + 1))
            if value >= beta:
                return value  # Beta cutoff
            alpha = max(alpha, value)
        best_value = value
        return value

    def MIN_VALUE(state, alpha, beta, depth):
        nonlocal best_move, best_value
        if depth >= max_depth or TERMINAL_TEST(state):
            return evaluation_function(state)
        
        value = float('inf')
        for child in state.children:
            # Call MAX_VALUE for the next level (maximizing player)
            value = min(value, MAX_VALUE(child, alpha, beta, depth + 1))
            if value <= alpha:
                return value  # Alpha cutoff
            beta = min(beta, value)
        best_value = value
        return value
    
    # Start with MAX_VALUE since the maximizing player (computer) moves first
    MAX_VALUE(state, -float('inf'), float('inf'), 0)
    
    # Choose the move corresponding to the best value found
    best_moves = [child for child in state.children if child.value == best_value]
    
    if best_moves:
        best_move = best_moves[0]  # Choose the first best move found
    
    return best_move
