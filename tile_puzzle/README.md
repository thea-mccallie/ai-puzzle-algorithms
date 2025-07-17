# Tile Puzzle Solver

This project implements a generalized sliding tile puzzle solver for boards of any size (rows x columns). The puzzle consists of numbered tiles and one empty space (represented by 0). The goal is to arrange the tiles in ascending order starting at the top-left corner and ending with the empty tile in the bottom-right corner, similar to the classic 8-puzzle.

---

## Features

- **Generalized board size:** Supports any rows × columns configuration.
- **Puzzle representation:** Board stored as a 2D list with integers, where `0` represents the empty space.
- **Movement:** Move the empty tile `"up"`, `"down"`, `"left"`, or `"right"` by swapping it with an adjacent tile.
- **Scramble:** Randomly applies valid moves to generate solvable puzzle states.
- **Solvers:**
  - **Iterative Deepening DFS (IDDFS):** Finds all optimal solutions by incrementally deepening the search depth.
  - **A* Search with Manhattan distance heuristic:** Efficiently finds one optimal solution.

---

## Running tests 

The project includes unit tests for all key functionality:
- Puzzle creation and initial state
- Move validity and effects
- Scrambling
- Checking solved state
- Successor generation
- IDDFS solver correctness
- A* solver correctness

Run tests with:
```python test_tile_puzzle.py```

