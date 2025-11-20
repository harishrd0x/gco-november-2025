#!/usr/bin/env python3
"""
Problem 6: Count total number of unique solutions for 5x5 grid with only C1 constraint
C1: No two orthogonally adjacent cells can contain consecutive numbers
No fixed seeds
"""

import sys
from typing import List, Set, Tuple, Optional

SIZE = 5
TOTAL_CELLS = SIZE * SIZE


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


def get_next_position(row: int, col: int) -> Tuple[int, int]:
    """Get next position in row-major order."""
    if col < SIZE - 1:
        return row, col + 1
    else:
        return row + 1, 0


def has_valid_placement(grid: List[List[int]], used: Set[int], row: int, col: int) -> bool:
    """Check if there's at least one valid value for this position."""
    for value in range(1, TOTAL_CELLS + 1):
        if value not in used and not violates_c1(grid, row, col, value):
            return True
    return False


def forward_check(grid: List[List[int]], used: Set[int], row: int, col: int) -> bool:
    """Forward checking: verify that all unassigned cells still have at least one valid value."""
    # Check next few positions to see if they still have valid placements
    # This is a simplified forward check - we check the immediate next position
    next_row, next_col = get_next_position(row, col)
    if next_row < SIZE:
        if not has_valid_placement(grid, used, next_row, next_col):
            return False
    return True


def solve_grid_count(grid: List[List[int]], used: Set[int], row: int, col: int) -> int:
    """Backtracking solver that counts all solutions with optimizations."""
    if row >= SIZE:
        return 1
    
    count = 0
    # Collect all valid values
    valid_values = []
    for value in range(1, TOTAL_CELLS + 1):
        if value not in used and not violates_c1(grid, row, col, value):
            valid_values.append(value)
    
    # If no valid values, backtrack immediately
    if not valid_values:
        return 0
    
    # Try each valid value
    for value in valid_values:
        grid[row][col] = value
        used.add(value)
        
        # Forward check: if next position has no valid values, skip this branch
        if forward_check(grid, used, row, col):
            next_row, next_col = get_next_position(row, col)
            count += solve_grid_count(grid, used, next_row, next_col)
        
        grid[row][col] = 0
        used.remove(value)
    
    return count


def main():
    grid = [[0] * SIZE for _ in range(SIZE)]
    used = set()
    
    count = solve_grid_count(grid, used, 0, 0)
    print(count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
