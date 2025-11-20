#!/usr/bin/env python3
"""
Problem 4: 5x5 Grid with C1, C2, C3, and C4 constraints
C4: Median of top row (Row 1) must be exactly 14
Output: Grid(5,5) value
"""

import sys
from typing import List, Set, Tuple

SIZE = 5
TOTAL_CELLS = SIZE * SIZE

# Prime-numbered positions (1-indexed, converted to 0-indexed)
PRIME_POSITIONS = [
    (0, 1), (0, 3),  # Row 1: Col 2, 4
    (1, 0), (1, 2),  # Row 2: Col 1, 3
    (2, 1), (2, 3),  # Row 3: Col 2, 4
    (3, 0), (3, 2),  # Row 4: Col 1, 3
    (4, 1), (4, 3),  # Row 5: Col 2, 4
]


def get_orthogonal_neighbors(row: int, col: int) -> List[Tuple[int, int]]:
    """Get orthogonally adjacent neighbors."""
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < SIZE and 0 <= nc < SIZE:
            neighbors.append((nr, nc))
    return neighbors


def get_diagonal_neighbors(row: int, col: int) -> List[Tuple[int, int]]:
    """Get diagonally adjacent neighbors."""
    neighbors = []
    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < SIZE and 0 <= nc < SIZE:
            neighbors.append((nr, nc))
    return neighbors


def violates_c1(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Check if placing value violates C1 (orthogonal consecutive constraint)."""
    for nr, nc in get_orthogonal_neighbors(row, col):
        neighbor_value = grid[nr][nc]
        if neighbor_value != 0:
            if abs(neighbor_value - value) == 1:
                return True
    return False


def violates_c2(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Check if placing value violates C2 (diagonal difference of 2 constraint)."""
    for nr, nc in get_diagonal_neighbors(row, col):
        neighbor_value = grid[nr][nc]
        if neighbor_value != 0:
            if abs(neighbor_value - value) == 2:
                return True
    return False


def check_c3(grid: List[List[int]]) -> bool:
    """Check if C3 constraint is satisfied (sum of prime positions is even)."""
    prime_sum = 0
    for row, col in PRIME_POSITIONS:
        value = grid[row][col]
        if value == 0:
            return True
        prime_sum += value
    return prime_sum % 2 == 0


def check_c4(grid: List[List[int]]) -> bool:
    """Check if C4 constraint is satisfied (median of top row = 14)."""
    top_row = grid[0]
    if any(val == 0 for val in top_row):
        return True  # Not all filled yet
    sorted_row = sorted(top_row)
    return sorted_row[2] == 14  # 3rd value (0-indexed: index 2)


def is_valid_placement(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Check if placing value at (row, col) is valid."""
    if violates_c1(grid, row, col, value):
        return False
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
    """Backtracking solver."""
    if row >= SIZE:
        if check_c3(grid) and check_c4(grid):
            return True
        return False
    
    for value in range(1, TOTAL_CELLS + 1):
        if value in used:
            continue
        
        if not is_valid_placement(grid, row, col, value):
            continue
        
        grid[row][col] = value
        used.add(value)
        
        # Early C3 check
        if all(grid[r][c] != 0 for r, c in PRIME_POSITIONS):
            if not check_c3(grid):
                grid[row][col] = 0
                used.remove(value)
                continue
        
        # Early C4 check (when top row is complete)
        if row == 0 and all(grid[0][c] != 0 for c in range(SIZE)):
            if not check_c4(grid):
                grid[row][col] = 0
                used.remove(value)
                continue
        
        next_row, next_col = get_next_position(row, col)
        if solve_grid(grid, used, next_row, next_col):
            return True
        
        grid[row][col] = 0
        used.remove(value)
    
    return False


def main():
    grid = [[0] * SIZE for _ in range(SIZE)]
    used = set()
    
    if solve_grid(grid, used, 0, 0):
        print(grid[4][4])  # Grid(5,5) = grid[4][4] (0-indexed)
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
