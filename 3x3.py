# 3x3.py - Edge Matching Puzzle Solver
from typing import List, Dict, Union

class GameGraph:
    def __init__(self, size=3):
        self.size = size
        self.num_nodes = size * size
        # Adjacency matrix for all nodes (0 = no connection, 1 = connected)
        self.graph = [[0 for _ in range(self.num_nodes)] for _ in range(self.num_nodes)]
        self._connect_adjacent_nodes()

    def _node_index(self, x, y):
        return x * self.size + y
    
    def _node_coordinates(self, index):
        x = index // self.size
        y = index % self.size
        return x, y

    def _connect_adjacent_nodes(self):
        for x in range(self.size):
            for y in range(self.size):
                idx = self._node_index(x, y)
                # Connect to right neighbor
                if y + 1 < self.size:
                    right_idx = self._node_index(x, y + 1)
                    self.graph[idx][right_idx] = 1
                    self.graph[right_idx][idx] = 1
                # Connect to bottom neighbor
                if x + 1 < self.size:
                    bottom_idx = self._node_index(x + 1, y)
                    self.graph[idx][bottom_idx] = 1
                    self.graph[bottom_idx][idx] = 1

    def add_edge(self, x1, y1, x2, y2):
        idx1 = self._node_index(x1, y1)
        idx2 = self._node_index(x2, y2)
        self.graph[idx1][idx2] = 1
        self.graph[idx2][idx1] = 1

    def remove_edge(self, x1, y1, x2, y2):
        idx1 = self._node_index(x1, y1)
        idx2 = self._node_index(x2, y2)
        self.graph[idx1][idx2] = 0
        self.graph[idx2][idx1] = 0

    def display(self):
        print(self.graph)

class Card:
    def __init__(self, sides: dict[int, tuple[str, bool]]):
        # sides: {0: ('color', is_front), 1: ('color', is_front), 2: ('color', is_front), 3: ('color', is_front)}
        # 0=top, 1=right, 2=bottom, 3=left
        if len(sides) != 4:
            raise ValueError("Card must have exactly 4 sides")
        self.sides = sides

    def get_side(self, side_index):
        """Get the color and orientation of a specific side (0=top, 1=right, 2=bottom, 3=left)"""
        return self.sides[side_index]

    def __repr__(self) -> str:
        return f"Card({self.sides})"

class CardCollection:
    def __init__(self, cards: Union[list[Card], dict[int, Card]], size=3):
        self.size = size
        if len(cards) != size * size:
            raise ValueError(f"Card collection must have exactly {size}^2 = {size * size} cards.")
        self.cards = cards if isinstance(cards, dict) else {i: cards[i] for i in range(size * size)}

    def __getitem__(self, index) -> Card:
        return self.cards[index]

    def __setitem__(self, index, value):
        self.cards[index] = value

    def __len__(self):
        return len(self.cards)

class Game:
    def __init__(self, size=3, cardCollection=None):
        self.size = size
        self.graph = GameGraph(size)
        self.cards = cardCollection.cards if cardCollection else {}
        self.solution = None

    def add_card(self, x, y, card):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.cards[x * self.size + y] = card

    def get_card(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.cards.get(x * self.size + y)
        return None

    def display_cards(self):
        for i in range(self.size):
            for j in range(self.size):
                card = self.get_card(i, j)
                if card:
                    print(f"Position ({i},{j}): {card}")
                else:
                    print(f"Position ({i},{j}): Empty")

    def is_valid_placement(self, x, y, card):
        """Check if placing a card at position (x,y) is valid"""
        # Check adjacent cards for matching edges
        directions = [
        (-1,  0, 0, 2),  # above:    our top (0)    vs their bottom (2)
        ( 0,  1, 1, 3),  # right:    our right (1)  vs their left   (3)
        ( 1,  0, 2, 0),  # below:    our bottom (2) vs their top    (0)
        ( 0, -1, 3, 1),  # left:     our left (3)   vs their right  (1)
        ]

        for dx, dy, card_side, adj_side in directions:
            adj_x, adj_y = x + dx, y + dy
            adjacent_card = self.get_card(adj_x, adj_y)
            
            if adjacent_card:
                # Get the side of our card that faces the adjacent card
                our_color, our_is_front = card.get_side(card_side)
                
                # Get the side of the adjacent card that faces us
                adj_color, adj_is_front = adjacent_card.get_side(adj_side)
                
                # They match if same color and opposite orientations
                if not (our_color == adj_color and our_is_front != adj_is_front):
                    return False
        
        return True

    def solve(self):
        """Solve the puzzle using backtracking"""
        if not self.cards:
            return False
            
        available_cards = list(self.cards.values())
        solution_grid = {}
        
        def backtrack(position):
            if position == self.size * self.size:
                return True
                
            x, y = position // self.size, position % self.size
            
            for i, card in enumerate(available_cards):
                if card is None:  # Already used
                    continue
                    
                # Try all 4 rotations
                for rotation in range(4):
                    # Create rotated card
                    rotated_sides = {}
                    for side in range(4):
                        rotated_sides[side] = card.get_side((side - rotation) % 4)
                    rotated_card = Card(rotated_sides)
                    
                    # Temporarily place the card for validation
                    solution_grid[position] = rotated_card
                    
                    # Check if this placement is valid
                    if self.is_valid_placement_in_grid(x, y, rotated_card, solution_grid):
                        available_cards[i] = None  # Mark as used
                        
                        if backtrack(position + 1):
                            return True
                            
                        # Backtrack
                        available_cards[i] = card  # Mark as available again
                    
                    # Remove the temporary placement
                    del solution_grid[position]
            
            return False
        
        if backtrack(0):
            self.solution = solution_grid
            return True
        return False

    def is_valid_placement_in_grid(self, x, y, card, grid):
        """Check if placing a card at position (x,y) is valid in the given grid"""
        position = x * self.size + y
        
        # Check adjacent cards for matching edges
        directions = [
        (-1,  0, 0, 2),  # above:    our top (0)    vs their bottom (2)
        ( 0,  1, 1, 3),  # right:    our right (1)  vs their left   (3)
        ( 1,  0, 2, 0),  # below:    our bottom (2) vs their top    (0)
        ( 0, -1, 3, 1),  # left:     our left (3)   vs their right  (1)
        ]

        for dx, dy, card_side, adj_side in directions:
            adj_x, adj_y = x + dx, y + dy
            adj_position = adj_x * self.size + adj_y
            
            # Check if adjacent position is within bounds and has a card
            if 0 <= adj_x < self.size and 0 <= adj_y < self.size and adj_position in grid:
                adjacent_card = grid[adj_position]
                
                # Get the side of our card that faces the adjacent card
                our_color, our_is_front = card.get_side(card_side)
                
                # Get the side of the adjacent card that faces us
                adj_color, adj_is_front = adjacent_card.get_side(adj_side)
                
                # They match if same color and opposite orientations
                if not (our_color == adj_color and our_is_front != adj_is_front):
                    return False
        
        return True

    def display_solution(self):
        """Display the solved puzzle using the visual format"""
        self.display_solution_visual()

    def format_side(self, color, is_front):
        """Format a side as color + orientation (1 for front, 0 for back)"""
        return f"{color}{1 if is_front else 0}"

    def display_card_visual(self, card, position_label=""):
        """Display a single card in visual format"""
        if not card:
            return ["     ", "     ", "     ", "     ", "     "]
        
        top = self.format_side(*card.get_side(0))
        right = self.format_side(*card.get_side(1))
        bottom = self.format_side(*card.get_side(2))
        left = self.format_side(*card.get_side(3))
          # Create a 5x5 representation of the card
        lines = [
            f"  {top:^3}  ",
            f"{left:<2}   {right:>2}",
            f"  {bottom:^3}  "
        ]
        return lines

    def display_solution_visual(self):
        """Display the solved puzzle in a nice visual grid format"""
        if not self.solution:
            print("No solution found!")
            return
            
        print("="*60)
        print("SOLUTION - Visual Grid:")
        print("="*60)
        print("Legend: Color + Orientation (1=front, 0=back)")
        print("Card sides: Top, Right, Bottom, Left")
        print("-"*60)
        
        # Display each row of the grid
        for row in range(self.size):
            # For each row, we need 3 lines (top, middle, bottom of cards)
            row_lines = [[], [], []]
            
            for col in range(self.size):
                position = row * self.size + col
                card = self.solution[position]
                pos_label = f"({row},{col})"
                card_lines = self.display_card_visual(card, pos_label)
                
                for i in range(3):
                    row_lines[i].append(card_lines[i])
            
            # Print the three lines for this row
            for line_parts in row_lines:
                print(" | ".join(line_parts))
            
            # Add separator between rows (except after last row)
            if row < self.size - 1:
                print("-" * (self.size * 11 + (self.size - 1) * 3))
        
        print("="*60)

    def display_cards_visual(self):
        """Display current card state in visual grid format"""
        print("="*60)
        print("CURRENT CARDS - Visual Grid:")
        print("="*60)
        print("Legend: Color + Orientation (1=front, 0=back)")
        print("Card sides: Top, Right, Bottom, Left")
        print("-"*60)
        
        # Display each row of the grid
        for row in range(self.size):
            # For each row, we need 3 lines (top, middle, bottom of cards)
            row_lines = [[], [], []]
            
            for col in range(self.size):
                card = self.get_card(row, col)
                pos_label = f"({row},{col})"
                card_lines = self.display_card_visual(card, pos_label)
                
                for i in range(3):
                    row_lines[i].append(card_lines[i])
            
            # Print the three lines for this row
            for line_parts in row_lines:
                print(" | ".join(line_parts))
            
            # Add separator between rows (except after last row)
            if row < self.size - 1:
                print("-" * (self.size * 11 + (self.size - 1) * 3))
        
        print("="*60)
        print()
        print()

    def debug_solution(self):
        """Debug the current solution to check if matches are correct"""
        if not self.solution:
            print("No solution to debug!")
            return
            
        print("\n🔍 DEBUGGING SOLUTION:")
        print("Checking adjacent card matches...")
        
        for row in range(self.size):
            for col in range(self.size):
                position = row * self.size + col
                card = self.solution[position]
                
                # Check right neighbor
                if col + 1 < self.size:
                    right_pos = row * self.size + (col + 1)
                    right_card = self.solution[right_pos]
                    
                    our_right = card.get_side(1)  # Right side
                    their_left = right_card.get_side(3)  # Left side
                    
                    match = (our_right[0] == their_left[0] and our_right[1] != their_left[1])
                    status = "✅" if match else "❌"
                    print(f"{status} ({row},{col}) right {our_right} <-> ({row},{col+1}) left {their_left}")
                
                # Check bottom neighbor  
                if row + 1 < self.size:
                    bottom_pos = (row + 1) * self.size + col
                    bottom_card = self.solution[bottom_pos]
                    
                    our_bottom = card.get_side(2)  # Bottom side
                    their_top = bottom_card.get_side(0)  # Top side
                    
                    match = (our_bottom[0] == their_top[0] and our_bottom[1] != their_top[1])
                    status = "✅" if match else "❌"
                    print(f"{status} ({row},{col}) bottom {our_bottom} <-> ({row+1},{col}) top {their_top}")

# Example usage
if __name__ == "__main__":
    # Example card collection with 9 cards
    # Each card has 4 sides: 0=top, 1=right, 2=bottom, 3=left
    # Each side has a tuple: (color, is_front_facing)
    cardCollection = CardCollection([
        Card({0: ('V', True), 1: ('R', True), 2: ('B', False), 3: ('Z', False)}),
        Card({0: ('Z', False), 1: ('R', True), 2: ('B', True), 3: ('R', False)}),
        Card({0: ('B', False), 1: ('V', True), 2: ('Z', True), 3: ('R', False)}),
        Card({0: ('R', False), 1: ('V', True), 2: ('B', True), 3: ('Z', False)}),        
        Card({0: ('B', False), 1: ('V', True), 2: ('Z', True), 3: ('R', False)}),
        Card({0: ('B', False), 1: ('V', True), 2: ('Z', True), 3: ('V', False)}),
        Card({0: ('B', False), 1: ('R', True), 2: ('V', True), 3: ('Z', False)}),
        Card({0: ('Z', False), 1: ('R', True), 2: ('B', True), 3: ('V', False)}),
        Card({0: ('B', False), 1: ('R', True), 2: ('Z', True), 3: ('V', False)}),
    ])

    # Create and solve the game
    game = Game(3, cardCollection)
    print("🧩 EDGE MATCHING PUZZLE SOLVER 🧩")
    print("Attempting to solve the puzzle...")    
    if game.solve():
        print("\n🎉 PUZZLE SOLVED! 🎉")
        game.display_solution()
        game.debug_solution()
    else:
        print("\n❌ No solution found for this puzzle.")