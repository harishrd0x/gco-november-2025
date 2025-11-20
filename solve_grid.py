#!/usr/bin/env python3
"""
Constraint Satisfaction Problem: 5x5 Grid Assignment

Constraints:
1. Fixed Seed: Center cell (3,3) = 13
2. C1 (Orthogonal): No two orthogonally adjacent cells can contain consecutive numbers
3. C2 (Diagonal): No two diagonally adjacent cells can contain numbers with difference of exactly 2
4. C3 (Prime/Even Sum): Sum of values in prime-numbered positions must be even

Prime positions (1-indexed): (1,2), (1,4), (2,1), (2,3), (3,2), (3,4), (4,1), (4,3), (5,2), (5,4)
"""

import sys
from typing import List, Set, Tuple, Optional

# Grid dimensions
SIZE = 5
TOTAL_CELLS = SIZE * SIZE

# Prime-numbered positions (1-indexed, converted to 0-indexed for internal use)
PRIME_POSITIONS = [
    (0, 1), (0, 3),  # Row 1: Col 2, 4
    (1, 0), (1, 2),  # Row 2: Col 1, 3
    (2, 1), (2, 3),  # Row 3: Col 2, 4
    (3, 0), (3, 2),  # Row 4: Col 1, 3
    (4, 1), (4, 3),  # Row 5: Col 2, 4
]

# Fixed center cell
CENTER_ROW, CENTER_COL = 2, 2  # 0-indexed (Row 3, Col 3)
CENTER_VALUE = 13


def is_prime_position(row: int, col: int) -> bool:
    """Check if a position (0-indexed) is a prime-numbered position."""
    return (row, col) in PRIME_POSITIONS


def get_orthogonal_neighbors(row: int, col: int) -> List[Tuple[int, int]]:
    """Get orthogonally adjacent neighbors (up, down, left, right)."""
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < SIZE and 0 <= nc < SIZE:
            neighbors.append((nr, nc))
    return neighbors


def get_diagonal_neighbors(row: int, col: int) -> List[Tuple[int, int]]:
    """Get diagonally adjacent neighbors (corners)."""
    neighbors = []
    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < SIZE and 0 <= nc < SIZE:
            neighbors.append((nr, nc))
    return neighbors


def violates_c1(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Check if placing value at (row, col) violates C1 (orthogonal consecutive constraint)."""
    for nr, nc in get_orthogonal_neighbors(row, col):
        neighbor_value = grid[nr][nc]
        if neighbor_value != 0:  # If neighbor is filled
            if abs(neighbor_value - value) == 1:
                return True
    return False


def violates_c2(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Check if placing value at (row, col) violates C2 (diagonal difference of 2 constraint)."""
    for nr, nc in get_diagonal_neighbors(row, col):
        neighbor_value = grid[nr][nc]
        if neighbor_value != 0:  # If neighbor is filled
            if abs(neighbor_value - value) == 2:
                return True
    return False


def check_c3(grid: List[List[int]]) -> bool:
    """Check if C3 constraint is satisfied (sum of prime positions is even)."""
    prime_sum = 0
    for row, col in PRIME_POSITIONS:
        value = grid[row][col]
        if value == 0:  # If any prime position is not filled, constraint not yet determined
            return True  # Don't fail yet, wait until all are filled
        prime_sum += value
    return prime_sum % 2 == 0


def is_valid_placement(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Check if placing value at (row, col) is valid according to all constraints."""
    # Check C1: Orthogonal consecutive constraint
    if violates_c1(grid, row, col, value):
        return False
    
    # Check C2: Diagonal difference of 2 constraint
    if violates_c2(grid, row, col, value):
        return False
    
    return True


def get_next_position(row: int, col: int) -> Tuple[int, int]:
    """Get next position in row-major order."""
    if col < SIZE - 1:
        return row, col + 1
    else:
        return row + 1, 0


def solve_grid(grid: List[List[int]], used: Set[int], row: int, col: int) -> bool:
    """
    Backtracking solver for the grid assignment problem.
    
    Args:
        grid: Current grid state (0 means unassigned)
        used: Set of values already used
        row, col: Current position to fill (0-indexed)
    
    Returns:
        True if solution found, False otherwise
    """
    # Base case: all cells filled
    if row >= SIZE:
        # Final check: C3 constraint (sum of prime positions must be even)
        if check_c3(grid):
            return True
        return False
    
    # Skip center cell (already fixed)
    if row == CENTER_ROW and col == CENTER_COL:
        next_row, next_col = get_next_position(row, col)
        return solve_grid(grid, used, next_row, next_col)
    
    # Try each unused value
    for value in range(1, TOTAL_CELLS + 1):
        if value in used:
            continue
        
        # Check if placement is valid
        if not is_valid_placement(grid, row, col, value):
            continue
        
        # Place value
        grid[row][col] = value
        used.add(value)
        
        # Early C3 check: if all prime positions are filled, verify constraint
        # This helps prune invalid branches early
        if all(grid[r][c] != 0 for r, c in PRIME_POSITIONS):
            if not check_c3(grid):
                # Constraint violated, backtrack
                grid[row][col] = 0
                used.remove(value)
                continue
        
        # Recursively solve next position
        next_row, next_col = get_next_position(row, col)
        if solve_grid(grid, used, next_row, next_col):
            return True
        
        # Backtrack
        grid[row][col] = 0
        used.remove(value)
    
    return False


def print_grid(grid: List[List[int]]):
    """Print grid in a readable format."""
    print("\nGrid:")
    for row in grid:
        print(" ".join(f"{val:3d}" for val in row))
    print()


def format_solution(grid: List[List[int]]) -> str:
    """Format solution as comma-separated string (row by row, left to right)."""
    result = []
    for row in grid:
        result.extend(str(val) for val in row)
    return ",".join(result)


def verify_solution(grid: List[List[int]]) -> bool:
    """Verify that the solution satisfies all constraints."""
    print("Verifying solution...")
    
    # Check all values 1-25 are used exactly once
    all_values = set()
    for row in grid:
        all_values.update(row)
    if all_values != set(range(1, 26)):
        print("ERROR: Not all values 1-25 are used!")
        return False
    print("✓ All values 1-25 used exactly once")
    
    # Check center cell
    if grid[CENTER_ROW][CENTER_COL] != CENTER_VALUE:
        print(f"ERROR: Center cell should be {CENTER_VALUE}, got {grid[CENTER_ROW][CENTER_COL]}")
        return False
    print(f"✓ Center cell is {CENTER_VALUE}")
    
    # Check C1: Orthogonal consecutive constraint
    for row in range(SIZE):
        for col in range(SIZE):
            value = grid[row][col]
            for nr, nc in get_orthogonal_neighbors(row, col):
                neighbor_value = grid[nr][nc]
                if abs(neighbor_value - value) == 1:
                    print(f"ERROR: C1 violation at ({row+1},{col+1})={value} and ({nr+1},{nc+1})={neighbor_value}")
                    return False
    print("✓ C1 (Orthogonal consecutive) constraint satisfied")
    
    # Check C2: Diagonal difference of 2 constraint
    for row in range(SIZE):
        for col in range(SIZE):
            value = grid[row][col]
            for nr, nc in get_diagonal_neighbors(row, col):
                neighbor_value = grid[nr][nc]
                if abs(neighbor_value - value) == 2:
                    print(f"ERROR: C2 violation at ({row+1},{col+1})={value} and ({nr+1},{nc+1})={neighbor_value}")
                    return False
    print("✓ C2 (Diagonal difference of 2) constraint satisfied")
    
    # Check C3: Prime positions sum is even
    prime_sum = sum(grid[r][c] for r, c in PRIME_POSITIONS)
    if prime_sum % 2 != 0:
        print(f"ERROR: C3 violation - sum of prime positions is {prime_sum} (odd)")
        return False
    print(f"✓ C3 (Prime positions sum is even) constraint satisfied: sum = {prime_sum}")
    
    return True


def main():
    """Main function to solve the grid assignment problem."""
    # Initialize grid (0 means unassigned)
    grid = [[0] * SIZE for _ in range(SIZE)]
    
    # Set center cell to 13
    grid[CENTER_ROW][CENTER_COL] = CENTER_VALUE
    used = {CENTER_VALUE}
    
    # Solve starting from position (0, 0)
    if solve_grid(grid, used, 0, 0):
        solution_str = format_solution(grid)
        print(solution_str)
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
