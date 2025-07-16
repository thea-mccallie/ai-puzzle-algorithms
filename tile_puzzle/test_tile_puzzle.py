import unittest
from tile_puzzle import create_tile_puzzle

class TestTilePuzzle(unittest.TestCase):

    def test_create_tile_puzzle(self):
        puzzle = create_tile_puzzle(2, 2)
        expected = [[1, 2], [3, 0]]
        self.assertEqual(puzzle.get_board(), expected)

    def test_perform_move_invalid(self):
        puzzle = create_tile_puzzle(2, 2)
        # Blank tile initially at bottom-right corner, cannot move down
        result = puzzle.perform_move("down")
        self.assertFalse(result)

        # Also test invalid direction string
        result = puzzle.perform_move("invalid_direction")
        self.assertFalse(result)

    def test_perform_move_up(self):
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
        puzzle = create_tile_puzzle(3, 3)
        puzzle.scramble(10)
        # After scrambling, puzzle should generally NOT be solved
        self.assertFalse(puzzle.is_solved())

    def test_is_solved_true(self):
        puzzle = create_tile_puzzle(2, 2)
        self.assertTrue(puzzle.is_solved())

    def test_is_solved_false(self):
        puzzle = create_tile_puzzle(2, 2)
        puzzle.perform_move("left")
        self.assertFalse(puzzle.is_solved())

    def test_successors(self):
        puzzle = create_tile_puzzle(2, 2)
        successors = list(puzzle.successors())
        self.assertTrue(len(successors) >= 2)  # At least 2 moves possible from start
        for move, new_puzzle in successors:
            self.assertNotEqual(new_puzzle.get_board(), puzzle.get_board())
            # Also, the move must be valid
            self.assertIn(move, ["up", "down", "left", "right"])

    def test_copy_independence(self):
        puzzle = create_tile_puzzle(2, 2)
        copy_puzzle = puzzle.copy()
        # Change original puzzle
        puzzle.perform_move("left")
        # Copy should remain unchanged
        self.assertNotEqual(puzzle.get_board(), copy_puzzle.get_board())

    def test_find_solutions_iddfs(self):
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
