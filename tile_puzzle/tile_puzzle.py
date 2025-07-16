import copy
import random
import queue
import itertools
import queue

'''
A tile puzzle game where the only possible moves are to swap the empty tile with one of its neighboring tiles. 
The goal state for the puzzle consists of tiles 1-3 in the top row, tiles 4-6 in the middle row, 
and tiles 7 and 8 in the bottom row, with the empty space in the lower-right corner.

Two solvers for a generalized version of the Eight Puzzle, in which the board can have any number of rows and columns
'''


def create_tile_puzzle(rows, cols):
    """
    Creates a solved tile puzzle board of size rows x cols.
    The board is a list of lists (matrix) with numbers from 1 to rows*cols - 1,
    and the bottom-right corner is set to 0 to represent the empty tile.
    Returns a TilePuzzle instance initialized with this board.
    """

    board = [] # matrix[row][col]

    for i in range(rows):
        row = []
        for j in range(cols):
            # Calculate tile number based on row and column
            tile_number = i * cols + j + 1
            row.append(tile_number)
        board.append(row)

    # Set the bottom-right corner tile to zero (empty space)
    board[rows - 1][cols - 1] = 0

    return TilePuzzle(board)

class TilePuzzle(object):
    
    def __init__(self, board):
        """
        Initialize the TilePuzzle with a given board
        """
        self.board = board
        # Number of columns (assuming rectangular board)
        self.cols = len(board[0]) if board else 0 # matrix[row][col]
        # Number of rows
        self.rows = len(board)

    def get_board(self):
        """
        Returns a deep copy of the current board state
        """
        return copy.deepcopy(self.board)

    def perform_move(self, direction):
        """
        Attempts to move the blank (0) tile in the given direction
        Returns True if the move is successful, False otherwise
        """
        # Find blank tile (0)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    row, col = i, j
                    break
            else:
                continue
            break

        # Movement directions
        change = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        if direction not in change:
            return False  # Invalid direction, off limits

        dr, dc = change[direction]
        new_row, new_col = row + dr, col + dc

        # Is the move within bounds?
        if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
            # Swap the blank with the target tile
            self.board[row][col], self.board[new_row][new_col] = self.board[new_row][new_col], self.board[row][col]
            return True

        return False  # Move out of bounds


    def scramble(self, num_moves):
        """
        Randomly completes valid moves on the puzzle to scramble it
        """
        moves = ["up", "down", "left", "right"]
        successful_moves = 0

        while successful_moves < num_moves:
            move = random.choice(moves)
            if self.perform_move(move):
                successful_moves += 1

    def is_solved(self):
        """
        Returns True if the puzzle is in the solved configuration
        """
        solved_board = [[i * self.cols + j + 1 for j in range(self.cols)] for i in range(self.rows)]
        solved_board[self.rows - 1][self.cols - 1] = 0
        return self.get_board() == solved_board

    def copy(self):
        """
        Return a new TilePuzzle object with a deep copy of the current board.
        """
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        """
        Generate all valid moves from the current puzzle state.
        Yields:
            (move: str, new_puzzle: TilePuzzle) for each valid move.
        """
        for move in ["up", "down", "left", "right"]:
            temp_board = self.copy()
            if temp_board.perform_move(move):  # Only yield if move succeeded
                yield (move, temp_board)


    def find_solutions_iddfs(self):
        """
        Solves the tile puzzle using Iterative Deepening Depth-First Search (IDDFS)
        Yields a list of moves (strings) that lead to the solved puzzle state
        """

        def recursive_dfs(puzzle, depth_limit, path, seen_states):
            """
            Recursively explore puzzle states up to a given depth
            """
            if puzzle.is_solved():
                yield path
                return

            if depth_limit == 0:
                return

            # Create a hashable version of the board to track visited states
            board_tuple = tuple(tuple(row) for row in puzzle.get_board())
            seen_states.add(board_tuple)

            for move in ["up", "down", "left", "right"]:
                next_puzzle = puzzle.copy()
                if next_puzzle.perform_move(move):
                    next_board_tuple = tuple(tuple(row) for row in next_puzzle.get_board())
                    if next_board_tuple not in seen_states:
                        yield from recursive_dfs(
                            next_puzzle,
                            depth_limit - 1,
                            path + [move],
                            seen_states
                        )

            # Backtrack so this state can be explored again in other paths
            seen_states.remove(board_tuple)

        # Main loop
        depth = 0
        while True:
            seen_states = set()
            for solution in recursive_dfs(self.copy(), depth, [], seen_states):
                yield solution
                return  # Stop after first found solution
            depth += 1


    def find_solution_a_star(self):
        """
        Solves the puzzle using the A* search algorithm with Manhattan distance as the heuristic
        Returns a list of moves that solves the puzzle from the current state
        """

        def manhattan_distance(board):
            """
            Computes the Manhattan distance of a board configuration from the goal state
            """
            distance = 0
            for row in range(self.rows):
                for col in range(self.cols):
                    tile = board[row][col]
                    if tile == 0:
                        continue
                    # Calculate target position for current tile
                    target_row = (tile - 1) // self.cols
                    target_col = (tile - 1) % self.cols
                    distance += abs(row - target_row) + abs(col - target_col)
            return distance

        start_state = self.copy()
        seen = set()
        tie_breaker = itertools.count()
        frontier = queue.PriorityQueue()

        initial_cost = manhattan_distance(start_state.get_board())
        frontier.put((initial_cost, 0, next(tie_breaker), start_state, []))

        while not frontier.empty():
            _, move_count, _, current_state, path = frontier.get()

            if current_state.is_solved():
                return path

            board_tuple = tuple(tuple(row) for row in current_state.get_board())
            if board_tuple in seen:
                continue
            seen.add(board_tuple)

            for move, successor in current_state.successors():
                successor_board = successor.get_board()
                successor_tuple = tuple(tuple(row) for row in successor_board)

                if successor_tuple not in seen:
                    g = move_count + 1
                    h = manhattan_distance(successor_board)
                    f = g + h
                    frontier.put((f, g, next(tie_breaker), successor, path + [move]))

        return None