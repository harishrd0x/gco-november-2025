#!/usr/bin/env python3
"""
Problem 6: Count total number of unique solutions for 5x5 grid with only C1 constraint
C1: No two orthogonally adjacent cells can contain consecutive numbers
No fixed seeds
Optimized version with precomputed neighbors and improved forward checking
"""

import sys
from typing import List, Set, Tuple

SIZE = 5
TOTAL_CELLS = SIZE * SIZE

# Precompute neighbor lists for all positions to avoid repeated calculations
NEIGHBORS: List[List[List[Tuple[int, int]]]] = [[[] for _ in range(SIZE)] for _ in range(SIZE)]
for row in range(SIZE):
    for col in range(SIZE):
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))
        if row < SIZE - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < SIZE - 1:
            neighbors.append((row, col + 1))
        NEIGHBORS[row][col] = neighbors


def violates_c1_fast(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Optimized C1 check using precomputed neighbors."""
    for nr, nc in NEIGHBORS[row][col]:
        neighbor_value = grid[nr][nc]
        if neighbor_value != 0 and abs(neighbor_value - value) == 1:
            return True
    return False


def get_next_position(row: int, col: int) -> Tuple[int, int]:
    """Get next position in row-major order."""
    if col < SIZE - 1:
        return row, col + 1
    else:
        return row + 1, 0


def has_valid_placement_fast(grid: List[List[int]], used: Set[int], row: int, col: int) -> bool:
    """Fast check if there's at least one valid value for this position."""
    # Check neighbors to get constraints
    forbidden = set()
    for nr, nc in NEIGHBORS[row][col]:
        neighbor_value = grid[nr][nc]
        if neighbor_value != 0:
            # Only add valid forbidden values (1-25 range)
            if neighbor_value > 1:
                forbidden.add(neighbor_value - 1)
            if neighbor_value < TOTAL_CELLS:
                forbidden.add(neighbor_value + 1)
    
    # Early exit: if all values are used or forbidden, return False
    if len(used) + len(forbidden) >= TOTAL_CELLS:
        # Check if there's any overlap between used and forbidden
        if used.isdisjoint(forbidden):
            return False
    
    # Check if any value is available and not forbidden
    for value in range(1, TOTAL_CELLS + 1):
        if value not in used and value not in forbidden:
            return True
    return False


def forward_check_improved(grid: List[List[int]], used: Set[int], row: int, col: int, depth: int = 2) -> bool:
    """Improved forward checking: verify next few positions have valid placements."""
    # Check next few positions to catch dead ends earlier
    check_row, check_col = row, col
    for _ in range(depth):
        check_row, check_col = get_next_position(check_row, check_col)
        if check_row >= SIZE:
            break
        if not has_valid_placement_fast(grid, used, check_row, check_col):
            return False
    return True


def solve_grid_count(grid: List[List[int]], used: Set[int], row: int, col: int) -> int:
    """Optimized backtracking solver that counts all solutions."""
    if row >= SIZE:
        return 1
    
    count = 0
    
    # Precompute forbidden values from neighbors for faster filtering
    forbidden = set()
    for nr, nc in NEIGHBORS[row][col]:
        neighbor_value = grid[nr][nc]
        if neighbor_value != 0:
            # Only add valid forbidden values (1-25 range)
            if neighbor_value > 1:
                forbidden.add(neighbor_value - 1)
            if neighbor_value < TOTAL_CELLS:
                forbidden.add(neighbor_value + 1)
    
    # Collect valid values more efficiently - iterate only over unused values
    # This avoids checking values we know are already used
    valid_values = []
    for value in range(1, TOTAL_CELLS + 1):
        if value not in used:
            # Quick check: if value is in forbidden set, skip
            if value not in forbidden:
                valid_values.append(value)
    
    # If no valid values, backtrack immediately
    if not valid_values:
        return 0
    
    # Compute next position once
    next_row, next_col = get_next_position(row, col)
    
    # Try each valid value
    for value in valid_values:
        grid[row][col] = value
        used.add(value)
        
        # If this is the last cell, we have a solution
        if next_row >= SIZE:
            count += 1
        # Otherwise, do forward checking and recurse
        elif forward_check_improved(grid, used, row, col, depth=2):
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
