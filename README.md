# 🧩 Edge Matching Puzzle Solver

A Python-based solver for edge matching puzzles (also known as "Scramble Squares", "Turtle Puzzles", or similar tile-matching games). This solver uses backtracking with rotation support to find valid arrangements of square tiles where adjacent edges must match.

## 🎯 What is an Edge Matching Puzzle?

Edge matching puzzles consist of square tiles that must be arranged in a grid (typically 3x3) such that:
- Adjacent tiles have matching edges
- Each edge has a **color/symbol** and an **orientation** (front/back)
- Two edges match if they have the **same color** but **opposite orientations**

For example: A `Red-Front` edge matches with a `Red-Back` edge.

## 🚀 Features

- ✅ **Solution Validation**: Built-in debugging to verify solution correctness
- ✅ **Flexible Grid Size**: Supports different grid sizes (default 3x3)

## 📋 Requirements

- Python 3.7+
- No external dependencies (uses only built-in libraries)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/edge-matching-puzzle-solver.git
cd edge-matching-puzzle-solver
```

2. Run the solver:
```bash
python 3x3.py
```

## 📖 Usage

### Basic Usage

The solver comes with an example puzzle. Simply run:

```bash
python 3x3.py
```

### Defining Your Own Puzzle

To solve your own puzzle, modify the `cardCollection` in the main section:

```python
# Each card has 4 sides: 0=top, 1=right, 2=bottom, 3=left
# Each side is a tuple: (color, is_front_facing)
cardCollection = CardCollection([
    Card({0: ('V', True), 1: ('R', True), 2: ('B', False), 3: ('Z', False)}),
    Card({0: ('Z', False), 1: ('R', True), 2: ('B', True), 3: ('R', False)}),
    # ... add all 9 cards for a 3x3 puzzle
])
```

### Card Definition Format

Each card is defined with a dictionary where:
- **Key**: Side number (0=top, 1=right, 2=bottom, 3=left)
- **Value**: Tuple of `(color, orientation)`
  - `color`: Any string identifier (e.g., 'R', 'B', 'V', 'Z')
  - `orientation`: Boolean (`True` = front-facing, `False` = back-facing)

### Example Card

```python
Card({
    0: ('Red', True),    # Top: Red front
    1: ('Blue', False),  # Right: Blue back  
    2: ('Green', True),  # Bottom: Green front
    3: ('Red', False)    # Left: Red back
})
```

## 🎮 Sample Output

```
🧩 EDGE MATCHING PUZZLE SOLVER 🧩
Attempting to solve the puzzle...

🎉 PUZZLE SOLVED! 🎉
============================================================
SOLUTION - Visual Grid:
============================================================
Legend: Color + Orientation (1=front, 0=back)
Card sides: Top, Right, Bottom, Left
------------------------------------------------------------
  Z0    |   R0    |   B0
B0 (0,0) V1 | Z0 (0,1) V1 | Z0 (0,2) R1
  R1    |   B1    |   V1
---------------------------------------
  B0    |   Z0    |   B0
V0 (1,0) R1 | V0 (1,1) R1 | R0 (1,2) V1
  Z1    |   B1    |   Z1
---------------------------------------
  B0    |   Z0    |   B0
R0 (2,0) V1 | R0 (2,1) R1 | V0 (2,2) V1
  Z1    |   B1    |   Z1
============================================================
```

## 🏗️ Code Structure

### Core Classes

- **`Card`**: Represents a single puzzle tile with 4 sides
- **`CardCollection`**: Manages a collection of cards for the puzzle
- **`Game`**: Main solver class with backtracking algorithm
- **`GameGraph`**: Adjacency graph for tile relationships (optional)

### Key Methods

- **`solve()`**: Main backtracking solver with rotation support
- **`is_valid_placement_in_grid()`**: Validates if a card placement is legal
- **`display_solution_visual()`**: Pretty-prints the solution grid
- **`debug_solution()`**: Validates and debugs the found solution

## 🔧 Customization

### Different Grid Sizes

```python
# For a 2x2 puzzle
cardCollection = CardCollection([...], size=2)
game = Game(2, cardCollection)

# For a 4x4 puzzle  
cardCollection = CardCollection([...], size=4)
game = Game(4, cardCollection)
```

### Custom Colors/Symbols

You can use any string identifiers for colors:

```python
Card({
    0: ('🐢', True),     # Turtle front
    1: ('🦅', False),    # Eagle back
    2: ('🐍', True),     # Snake front
    3: ('🐸', False)     # Frog back
})
```

## 🐛 Debugging

The solver includes built-in debugging. If a solution seems incorrect, the debug output will show:

```
🔍 DEBUGGING SOLUTION:
Checking adjacent card matches...
✅ (0,0) right ('V', True) <-> (0,1) left ('V', False)
❌ (0,1) right ('R', True) <-> (0,2) left ('B', False)
```

- ✅ = Valid match (same color, opposite orientations)
- ❌ = Invalid match (different colors or same orientations)

## 🚀 Future Enhancements

This solver could be expanded with:

- [ ] **GUI Interface**: Visual puzzle editor and solver
- [ ] **Image Recognition**: Load puzzles from photos
- [ ] **Multiple Solutions**: Find all possible solutions
- [ ] **Performance Optimization**: Constraint propagation, heuristics
- [ ] **Puzzle Generator**: Create new solvable puzzles
- [ ] **Different Tile Shapes**: Hexagonal, triangular tiles
- [ ] **Web Interface**: Browser-based solver
- [ ] **Solution Animation**: Step-by-step solving visualization

## 📝 Algorithm Details

### Backtracking Process

1. **Placement**: Try each available card at the current position
2. **Rotation**: For each card, try all 4 rotations (0°, 90°, 180°, 270°)
3. **Validation**: Check if the rotated card matches all adjacent cards
4. **Recursion**: If valid, move to next position; if not, backtrack
5. **Solution**: Found when all positions are filled with valid placements

### Edge Matching Logic

Two adjacent edges match if:
```python
edge1_color == edge2_color and edge1_orientation != edge2_orientation
```

### Rotation Implementation

Rotation is achieved by shifting the side indices:
```python
# 90° clockwise rotation
rotated_sides[side] = original_card.get_side((side - 1) % 4)
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Performance optimizations
- Additional puzzle formats
- Better visualization
- Test cases and examples
- Documentation improvements

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

Inspired by classic edge-matching puzzles like Scramble Squares and similar tile-matching games.

---

**Happy Puzzling!** 🧩✨
