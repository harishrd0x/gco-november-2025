#!/usr/bin/env python3
"""
Problem 6: Count total number of unique solutions for 5x5 grid with only C1 constraint
C1: No two orthogonally adjacent cells can contain consecutive numbers
No fixed seeds
"""

import sys
from typing import List, Set, Tuple

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


def solve_grid_count(grid: List[List[int]], used: Set[int], row: int, col: int) -> int:
    """Backtracking solver that counts all solutions."""
    if row >= SIZE:
        return 1
    
    count = 0
    for value in range(1, TOTAL_CELLS + 1):
        if value in used:
            continue
        
        if violates_c1(grid, row, col, value):
            continue
        
        grid[row][col] = value
        used.add(value)
        
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
