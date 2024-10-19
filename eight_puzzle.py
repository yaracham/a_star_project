import numpy as np

class EightPuzzle:
    def __init__(self, initial_state):
        self.state = np.array(initial_state)
        self.blank_pos = tuple(np.argwhere(self.state == 0)[0])  # Convert to tuple for consistency

    def move(self, direction):
        """Move the blank tile in the specified direction, if possible."""
        row, col = self.blank_pos
        if direction == 'up' and row > 0:
            self._swap((row, col), (row - 1, col))
        elif direction == 'down' and row < 2:
            self._swap((row, col), (row + 1, col))
        elif direction == 'left' and col > 0:
            self._swap((row, col), (row, col - 1))
        elif direction == 'right' and col < 2:
            self._swap((row, col), (row, col + 1))

    def _swap(self, pos1, pos2):
        """Swap two positions in the puzzle."""
        self.state[pos1], self.state[pos2] = self.state[pos2], self.state[pos1]
        self.blank_pos = pos2  # Update the blank position

    def is_solved(self):
        """Check if the puzzle is solved."""
        goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        return np.array_equal(self.state, goal_state)

    def copy(self):
        """Return a copy of the current puzzle."""
        return EightPuzzle(self.state.copy())

    def legal_moves(self):
        """Return a list of legal moves from the current state."""
        row, col = self.blank_pos
        moves = []
        if row > 0:
            moves.append('up')
        if row < 2:
            moves.append('down')
        if col > 0:
            moves.append('left')
        if col < 2:
            moves.append('right')
        return moves

    def result(self, move):
        """Return the resulting state from applying a move."""
        new_puzzle = self.copy()
        new_puzzle.move(move)
        return new_puzzle

    def __eq__(self, other):
        """Check if two puzzle states are equal."""
        return isinstance(other, EightPuzzle) and np.array_equal(self.state, other.state)

    def __hash__(self):
        """Allow the puzzle state to be hashed for use in sets and dictionaries."""
        return hash(self.state.tobytes())  # Convert to bytes for consistent hashing

    def __str__(self):
        """String representation of the puzzle state."""
        return '\n'.join([' '.join(map(str, row)) for row in self.state]) + '\n'

    def __lt__(self, other):
        """Define a less-than comparison for priority queue usage, comparing using heuristics."""
        from heuristics import manhattan_distance  # Import heuristic dynamically
        return manhattan_distance(self) < manhattan_distance(other)