#!/usr/bin/env python3
"""
Problem 5: 6x6 Grid with fixed seed (1,1)=1, C1, and C5 (Rook constraint)
C5: No two numbers from {1, 12, 24, 36} can be in the same row or column
Output: Comma-separated string of 36 integers
"""

import sys
from typing import List, Set, Tuple

SIZE = 6
TOTAL_CELLS = SIZE * SIZE

# Special numbers for C5 constraint
SPECIAL_NUMBERS = {1, 12, 24, 36}

# Fixed seed: (1,1) = 1 (0-indexed: (0,0) = 1)
FIXED_ROW, FIXED_COL = 0, 0
FIXED_VALUE = 1


def get_orthogonal_neighbors(row: int, col: int) -> List[Tuple[int, int]]:
    """Get orthogonally adjacent neighbors."""
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
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


def violates_c5(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Check if placing value violates C5 (Rook constraint)."""
    if value not in SPECIAL_NUMBERS:
        return False
    
    # Check same row
    for c in range(SIZE):
        if c != col and grid[row][c] != 0:
            if grid[row][c] in SPECIAL_NUMBERS:
                return True
    
    # Check same column
    for r in range(SIZE):
        if r != row and grid[r][col] != 0:
            if grid[r][col] in SPECIAL_NUMBERS:
                return True
    
    return False


def is_valid_placement(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Check if placing value at (row, col) is valid."""
    if violates_c1(grid, row, col, value):
        return False
    if violates_c5(grid, row, col, value):
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
        return True
    
    # Skip fixed cell
    if row == FIXED_ROW and col == FIXED_COL:
        next_row, next_col = get_next_position(row, col)
        return solve_grid(grid, used, next_row, next_col)
    
    for value in range(1, TOTAL_CELLS + 1):
        if value in used:
            continue
        
        if not is_valid_placement(grid, row, col, value):
            continue
        
        grid[row][col] = value
        used.add(value)
        
        next_row, next_col = get_next_position(row, col)
        if solve_grid(grid, used, next_row, next_col):
            return True
        
        grid[row][col] = 0
        used.remove(value)
    
    return False


def format_solution(grid: List[List[int]]) -> str:
    """Format solution as comma-separated string (row by row, left to right)."""
    result = []
    for row in grid:
        result.extend(str(val) for val in row)
    return ",".join(result)


def main():
    grid = [[0] * SIZE for _ in range(SIZE)]
    grid[FIXED_ROW][FIXED_COL] = FIXED_VALUE
    used = {FIXED_VALUE}
    
    if solve_grid(grid, used, 0, 0):
        print(format_solution(grid))
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
