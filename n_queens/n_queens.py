import math

"""
A solver for the n-queens problem, wherein n queens are to be placed on an n x n chessboard 
so that no pair of queens can attack each other
"""

def num_placements_all(n):
    # The number of possible placements of n queens on an n x n board 
    # where all queens are indistinguishable 
    # WITHOUT restriction of queens per row

    return math.comb(n * n, n)

def num_placements_one_per_row(n):
    # The number of possible placements of n queens on an n x n board 
    # where all queens are indistinguishable 
    # WITH restriction of queens per row 

    return n ** n


def n_queens_valid(board):
    # Time complexity: O(n)

    # Accepts a list where the ith number designates the column of the queen in row i for 0 ≤ i < n
    # and returns True if no queen can attack another, or False otherwise

    # Queens can attack each other if they are in the same column or on the same diagonal

    seen_cols = set()
    seen_dips = set()  # row - col, decreasing diagonal from left to right
    seen_rises = set()  # row + col, increasing diagonal from left to right

    # Diagonal dips and rises illustration on a 5x5 board:

    # Dips                      Rises
    # 0 -1 -2 -3 -4             0  1  2  3  4
    # 1  0 -1 -2 -3             1  2  3  4  5
    # 2  1  0 -1 -2             2  3  4  5  6
    # 3  2  1  0 -1             3  4  5  6  7
    # 4  3  2  1  0             4  5  6  7  8

    for row, col in enumerate(board):
        if col in seen_cols or (row - col) in seen_dips or (row + col) in seen_rises:
            return False

        seen_cols.add(col)
        seen_dips.add(row - col)
        seen_rises.add(row + col)

    return True

def n_queens_solutions(n: int):
    # Worst-case time complexity: O(n!)

    # Sets to keep track of columns and diagonals where queens are already placed
    cols = set()
    dips = set()   # row - col
    rises = set()  # row + col
    # List to represent the current board state; board[row] = col of queen
    board = [None] * n

    def backtrack(row: int):

        """
        Try to place a queen in `row` and recursively solve for next rows.
        Yields all valid board configurations.
        """
        
        # Base case - all rows have been processed
        # Yield a copy of the current board (which has determined to be the solution)
        if row == n:
            yield list(board)
            return

        # Try placing the queen in each column of the current row
        for col in range(n):
            # A queen is safe if:
            # The column is not already occupied
            # The decreasing diagonal (row - col) is not already occupied
            # The increasing diagonal (row + col) is not already occupied
            if (col in cols) or ((row - col) in dips) or ((row + col) in rises):
                continue

            # Mark the queen's position, log the column and diagonals used
            cols.add(col)
            dips.add(row - col)
            rises.add(row + col)
            board[row] = col

            yield from backtrack(row + 1) # Recurse

            # Backtrack to explore other placements by removing the queen 
            # and unmarking the column and diagonals
            cols.remove(col)
            dips.remove(row - col)
            rises.remove(row + col)
            board[row] = None

    yield from backtrack(0) # Backtracking begins from the first row


# Bonus function to return all solutions as a list
# Not included in original assignment
def n_queens_solutions_all(n: int):
    # Worst-case time complexity: O(n!)

    solutions = []

    for solution in n_queens_solutions(n):
        solutions.append(solution)

    return solutions
