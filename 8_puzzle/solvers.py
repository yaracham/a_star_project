from collections import deque
import heapq

# BFS Solver
def bfs_solve(puzzle):
    """Solve the 8-puzzle using BFS and return the sequence of moves."""
    frontier = deque([(puzzle.copy(), [])])  # Queue of (puzzle, moves)
    explored = set()
    explored_nodes = 0

    while frontier:
        current_puzzle, moves = frontier.popleft()

        if current_puzzle.is_solved():
            return moves, explored_nodes  # Return the list of moves to solve the puzzle and explored nodes

        if current_puzzle not in explored:
            explored.add(current_puzzle)
            explored_nodes += 1

            for move in current_puzzle.legal_moves():
                new_puzzle = current_puzzle.result(move)
                frontier.append((new_puzzle, moves + [move]))

    return [], explored_nodes  # No solution found

# A* Solver
def a_star_solve(puzzle, heuristic):
    """Solve the 8-puzzle using the A* algorithm and return the sequence of moves."""
    frontier = []  # Priority queue (min-heap)
    heapq.heappush(frontier, (heuristic(puzzle), 0, puzzle.copy(), []))  # (priority, cost, puzzle, moves)
    explored = set()
    explored_nodes = 0

    while frontier:
        _, cost, current_puzzle, moves = heapq.heappop(frontier)

        if current_puzzle.is_solved():
            return moves, explored_nodes  # Return the list of moves to solve the puzzle and explored nodes

        if current_puzzle not in explored:
            explored.add(current_puzzle)
            explored_nodes += 1

            for move in current_puzzle.legal_moves():
                new_puzzle = current_puzzle.result(move)
                new_moves = moves + [move]
                new_cost = cost + 1  # Each move has a cost of 1
                priority = new_cost + heuristic(new_puzzle)  # f(n) = g(n) + h(n)
                heapq.heappush(frontier, (priority, new_cost, new_puzzle, new_moves))

    return [], explored_nodes  # No solution found

