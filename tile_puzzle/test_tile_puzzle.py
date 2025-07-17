import unittest
from tile_puzzle import create_tile_puzzle

"""
Generalized Tile Puzzle solver supporting arbitrary board sizes.
Includes move logic, scrambling, and puzzle state tracking.
Solves puzzles using IDDFS and A* search with Manhattan distance.
Inspired by the classic 8-puzzle with a movable empty tile (0).
"""

class TestTilePuzzle(unittest.TestCase):

    def test_create_tile_puzzle(self):
        """ Tests that create_tile_puzzle initializes a puzzle with the correct solved board configuration """
        # Time complexity: O(r × c)
        # r is rows, c is columns

        puzzle = create_tile_puzzle(2, 2)
        expected = [[1, 2], [3, 0]]
        self.assertEqual(puzzle.get_board(), expected)

    def test_perform_move_invalid(self):
        """ Tests that perform_move correctly returns False for invalid directions or moves that go out of bounds """
        # Time complexity: O(1)
        puzzle = create_tile_puzzle(2, 2)
        # Blank tile initially at bottom-right corner, cannot move down
        result = puzzle.perform_move("down")
        self.assertFalse(result)

        # Also test invalid direction string
        result = puzzle.perform_move("invalid_direction")
        self.assertFalse(result)

    def test_perform_move_up(self):
        """ Tests that perform_move successfully moves the blank tile up and left, updating the board correctly """
        # Time complexity: O(1)

        puzzle = create_tile_puzzle(2, 2)
        # Move blank left first (valid)
        self.assertTrue(puzzle.perform_move("left"))
        # Then move blank up (valid)
        result = puzzle.perform_move("up")
        self.assertTrue(result)
        # Expected board after moves: blank at top-left
        expected = [[0, 2], [1, 3]]
        self.assertEqual(puzzle.get_board(), expected)

    def test_perform_move_edge_cases(self):
        """ Tests perform_move behavior on edge cases where moves are valid or invalid at board boundaries """
        # Time complexity: O(1)

        puzzle = create_tile_puzzle(2, 2)
        # Move blank left (valid)
        self.assertTrue(puzzle.perform_move("left"))
        # Try moving left again (invalid, blank at left edge)
        self.assertFalse(puzzle.perform_move("left"))
        # Move up (valid)
        self.assertTrue(puzzle.perform_move("up"))
        # Try moving up again (invalid, blank at top edge)
        self.assertFalse(puzzle.perform_move("up"))

    def test_scramble(self):
        """ Tests that scrambling the puzzle alters its state so it is typically not solved afterward"""
        # Time complexity: O(k)
        # k is the number of moves to scramble

        puzzle = create_tile_puzzle(3, 3)
        puzzle.scramble(10)
        # After scrambling, puzzle should generally NOT be solved
        # But check anyway
        self.assertFalse(puzzle.is_solved())

    def test_is_solved_true(self):
        """ Tests that a newly created puzzle is recognized as solved """
        # Time complexity: O(r × c)
        # r is rows, c is columns

        puzzle = create_tile_puzzle(2, 2)
        self.assertTrue(puzzle.is_solved())

    def test_is_solved_false(self):
        """ Tests that the puzzle is correctly identified as not solved after a valid move """
        # Time complexity: O(r × c)
        # r is rows, c is columns

        puzzle = create_tile_puzzle(2, 2)
        puzzle.perform_move("left")
        self.assertFalse(puzzle.is_solved())

    def test_successors(self):
        """ Tests that successors generates valid and distinct puzzle states for all possible moves"""
        # Time complexity: O(m)
        # m is the number of valid moves from the current state

        puzzle = create_tile_puzzle(2, 2)
        successors = list(puzzle.successors())
        self.assertTrue(len(successors) >= 2)  # There are at least 2 moves possible from start
        for move, new_puzzle in successors:
            self.assertNotEqual(new_puzzle.get_board(), puzzle.get_board())
            # Also, the move must be valid
            self.assertIn(move, ["up", "down", "left", "right"])

    def test_copy_independence(self):
        """ Tests that modifying the original puzzle does not affect its copied instance """
        # Time complexity: O(r × c)
        # r is rows, c is columns

        puzzle = create_tile_puzzle(2, 2)
        copy_puzzle = puzzle.copy()
        # Change original puzzle
        puzzle.perform_move("left")
        # Copy should remain unchanged
        self.assertNotEqual(puzzle.get_board(), copy_puzzle.get_board())

    def test_find_solutions_iddfs(self):
        """ Tests that find_solutions_iddfs returns valid move sequences that solve the puzzle """
        # TIme complexity: worst case O(b^d)
        # b is branching factor, d is depth of solution

        puzzle = create_tile_puzzle(2, 2)
        puzzle.perform_move("left")  # Make puzzle unsolved
        solutions = list(puzzle.find_solutions_iddfs())

        def apply_moves(puzzle_obj, moves):
            p = puzzle_obj.copy()
            for move in moves:
                p.perform_move(move)
            return p

        # At least one returned solution should solve the puzzle when applied
        self.assertTrue(any(apply_moves(puzzle, seq).is_solved() for seq in solutions))

    def test_find_solution_a_star(self):
        """ Tests that find_solution_a_star returns a valid move sequence that solves the puzzle """
        # Time complexity: O(b^d) in worst case, but not likely
        puzzle = create_tile_puzzle(2, 2)
        puzzle.perform_move("left")
        path = puzzle.find_solution_a_star()
        self.assertIsNotNone(path)
        self.assertIsInstance(path, list)

        # Apply the returned moves on a fresh copy to verify solution
        test_puzzle = puzzle.copy()
        for move in path:
            test_puzzle.perform_move(move)
        self.assertTrue(test_puzzle.is_solved())

if __name__ == '__main__':
    unittest.main()
