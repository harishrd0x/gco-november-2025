#!/usr/bin/env python3
"""
Problem 6: Count the number of 5x5 grids (values 1..25) that satisfy C1.
C1: Any orthogonally adjacent pair of cells must NOT contain consecutive numbers.
"""

from typing import List, Tuple

SIZE = 5
TOTAL_CELLS = SIZE * SIZE
ALL_NUMBER_MASK = (1 << TOTAL_CELLS) - 1


def _build_neighbor_map(size: int) -> List[Tuple[int, ...]]:
    """Return orthogonal neighbors for every linearized cell index."""
    neighbors: List[Tuple[int, ...]] = []
    for row in range(size):
        for col in range(size):
            idx = row * size + col
            cell_neighbors = []
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = row + dr, col + dc
                if 0 <= nr < size and 0 <= nc < size:
                    cell_neighbors.append(nr * size + nc)
            neighbors.append(tuple(cell_neighbors))
    return neighbors


def _build_adjacent_value_forbid(total_values: int) -> List[int]:
    """
    For every value v (1-indexed), precompute a bitmask containing the values
    that cannot be placed in an orthogonal neighbor (i.e. v-1 and/or v+1).
    """
    forbid_masks = [0] * (total_values + 1)
    for value in range(1, total_values + 1):
        mask = 0
        if value > 1:
            mask |= 1 << (value - 2)
        if value < total_values:
            mask |= 1 << value
        forbid_masks[value] = mask
    return forbid_masks


NEIGHBORS = _build_neighbor_map(SIZE)
ADJACENT_VALUE_FORBID = _build_adjacent_value_forbid(TOTAL_CELLS)


def _select_position(unassigned_mask: int, available_mask: int, forbidden_masks: List[int]) -> Tuple[int, int]:
    """
    Choose the next cell to fill using a minimum-remaining-values heuristic.
    Returns a tuple of (position index, domain bitmask). If any cell has an
    empty domain, it is returned immediately to enable quick backtracking.
    """
    best_pos = -1
    best_domain = 0
    best_size = TOTAL_CELLS + 1
    mask = unassigned_mask

    while mask:
        bit = mask & -mask
        pos = bit.bit_length() - 1
        domain = available_mask & (~forbidden_masks[pos] & ALL_NUMBER_MASK)
        domain_size = domain.bit_count()

        if domain_size == 0:
            return pos, 0
        if domain_size < best_size:
            best_size = domain_size
            best_pos = pos
            best_domain = domain
            if domain_size == 1:
                break
        mask ^= bit

    return best_pos, best_domain


def count_valid_grids() -> int:
    """
    Count all assignments via bitset-based backtracking with MRV ordering and
    incremental constraint propagation.
    """
    forbidden_masks = [0] * TOTAL_CELLS

    def dfs(unassigned_mask: int, available_mask: int) -> int:
        if unassigned_mask == 0:
            return 1

        pos, domain = _select_position(unassigned_mask, available_mask, forbidden_masks)
        if domain == 0:
            return 0

        next_unassigned_mask = unassigned_mask & ~(1 << pos)
        total = 0

        while domain:
            value_bit = domain & -domain
            domain ^= value_bit
            value = value_bit.bit_length()

            added_forbids = []
            forbid_bits = ADJACENT_VALUE_FORBID[value]
            if forbid_bits:
                for neighbor in NEIGHBORS[pos]:
                    prev_mask = forbidden_masks[neighbor]
                    new_mask = prev_mask | forbid_bits
                    if new_mask != prev_mask:
                        forbidden_masks[neighbor] = new_mask
                        added_forbids.append((neighbor, prev_mask))

            total += dfs(next_unassigned_mask, available_mask ^ value_bit)

            for neighbor, prev_mask in reversed(added_forbids):
                forbidden_masks[neighbor] = prev_mask

        return total

    full_mask = (1 << TOTAL_CELLS) - 1
    return dfs(full_mask, full_mask)


def main() -> int:
    print(count_valid_grids())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
