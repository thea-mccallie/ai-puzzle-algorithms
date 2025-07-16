import unittest
from n_queens import (
    num_placements_all,
    num_placements_one_per_row,
    n_queens_valid,
    n_queens_solutions
)

class TestNQueens(unittest.TestCase):

    # Test the total number of placements of N identical queens on an n x n board
    # No constraints about row or column placement
    def test_num_placements_all(self):
        self.assertEqual(num_placements_all(0), 1)
        self.assertEqual(num_placements_all(1), 1)
        self.assertEqual(num_placements_all(2), 6)
        self.assertEqual(num_placements_all(3), 84)
        self.assertEqual(num_placements_all(4), 1820)
        self.assertEqual(num_placements_all(5), 53130)
        self.assertEqual(num_placements_all(6), 1947792)

    # Test the number of placements with exactly one identical queen per row
    # No contrants about column placement or diagonal attacks
    def test_num_placements_one_per_row(self):
        self.assertEqual(num_placements_one_per_row(0), 1)  # 0^0 in Python is treated as 1
        self.assertEqual(num_placements_one_per_row(1), 1)
        self.assertEqual(num_placements_one_per_row(2), 4)
        self.assertEqual(num_placements_one_per_row(3), 27)
        self.assertEqual(num_placements_one_per_row(4), 256)
        self.assertEqual(num_placements_one_per_row(5), 3125)
        self.assertEqual(num_placements_one_per_row(6), 46656)


    # Test if n_queens_valid correctly recognizes valid board configurations
    def test_n_queens_valid(self):
        # Valid boards
        self.assertTrue(n_queens_valid([]))
        self.assertTrue(n_queens_valid([0]))
        self.assertTrue(n_queens_valid([1, 3, 0, 2]))
        self.assertTrue(n_queens_valid([2, 0, 3, 1]))
        self.assertTrue(n_queens_valid([3, 1, 4, 2, 0]))

        # Invalid (same column)
        self.assertFalse(n_queens_valid([0, 0]))
        self.assertFalse(n_queens_valid([2, 1, 2]))

        # Invalid (diagonal violation)
        self.assertFalse(n_queens_valid([0, 2, 1]))
        self.assertFalse(n_queens_valid([1, 3, 1]))
        self.assertFalse(n_queens_valid([0, 1, 2, 3]))


    # Test if n_queens_solutions(n) returns the correct number of valid solutions
    def test_n_queens_solutions(self):
        self.assertEqual(len(list(n_queens_solutions(1))), 1)
        self.assertEqual(len(list(n_queens_solutions(2))), 0)
        self.assertEqual(len(list(n_queens_solutions(3))), 0)
        self.assertEqual(len(list(n_queens_solutions(4))), 2)
        self.assertEqual(len(list(n_queens_solutions(5))), 10)
        self.assertEqual(len(list(n_queens_solutions(6))), 4)

if __name__ == "__main__":
    unittest.main()