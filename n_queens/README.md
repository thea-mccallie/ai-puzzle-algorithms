# 🧠 N-Queens Solver

This project provides a Python implementation of a solver for the classic **N-Queens problem**, where `n` queens must be placed on an `n × n` chessboard so that no two queens threaten each other.

It includes:
- Efficient solution generation using backtracking
- Board configuration validation
- Utility functions for counting different types of placements
- Unit tests to verify correctness

---

### 🔁 Running the Solver

python test_n_queens.py

---

## 📚 Included Functions
```num_placements_all(n)```
Returns the number of ways to place n identical queens on an n x n board with no restrictions.

```num_placements_one_per_row(n)```
Returns the number of placements with one queen per row (but still allows conflicts).

```n_queens_valid(board)```
Validates a board configuration (list of column positions by row). Returns True if no queens attack each other.

```n_queens_solutions(n)```
A generator that yields all valid board configurations that solve the N-Queens problem.

```n_queens_solutions_all(n)```
Returns all valid N-Queens solutions in a list (helper built on top of the generator).

---

 ## 🧪 Sample Output

```list(n_queens_solutions(4))```
[[1, 3, 0, 2], [2, 0, 3, 1]]

```n_queens_valid([1, 3, 0, 2])```
True

```num_placements_all(3)```
84
