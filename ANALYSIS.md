# Problem Analysis: 5x5 Grid Constraint Satisfaction

## Problem Overview

Find a valid assignment of numbers 1-25 (each used exactly once) to a 5×5 grid satisfying:
1. **Fixed Seed**: Center cell (3,3) = 13
2. **C1 (Orthogonal)**: No orthogonally adjacent cells can contain consecutive numbers
3. **C2 (Diagonal)**: No diagonally adjacent cells can contain numbers with difference of exactly 2
4. **C3 (Prime/Even Sum)**: Sum of values in 10 prime-numbered positions must be even

## Why This Problem is Challenging

### Constraint Interactions
- **C1** restricts local placements: if a cell has value N, its 4 orthogonal neighbors cannot be N-1 or N+1
- **C2** restricts diagonal placements: if a cell has value N, its 4 diagonal neighbors cannot be N±2
- **C3** is a global constraint: the sum of 10 specific positions must be even, which depends on the entire assignment

### Search Space
- Without constraints: 25! ≈ 1.55×10²⁵ possible assignments
- With fixed center: 24! ≈ 6.2×10²³
- With all constraints: Significantly reduced, but still requires systematic search

## Algorithmic Approach: Backtracking with Constraint Propagation

### Why Backtracking?
1. **Systematic Exploration**: Guarantees finding a solution if one exists
2. **Early Pruning**: Invalid partial assignments are discarded immediately
3. **Constraint Checking**: Each placement is validated against all applicable constraints

### Key Design Decisions

#### 1. Constraint Checking Strategy
- **C1 & C2**: Checked immediately when placing a value (local constraints)
- **C3**: Checked when all prime positions are filled (global constraint)
- This allows early pruning of invalid branches

#### 2. Search Order
- **Row-major order**: Fill cells left-to-right, top-to-bottom
- **Value ordering**: Try values 1-25 in ascending order
- This provides a deterministic search path

#### 3. Early Termination
- Once all prime positions are filled, verify C3 immediately
- If violated, backtrack without exploring further
- Reduces unnecessary computation

### Why This Works

1. **Constraint Propagation**: Each placement immediately restricts future placements in adjacent cells
2. **Incremental Validation**: Constraints are checked as soon as enough information is available
3. **Backtracking Efficiency**: Invalid paths are abandoned early, avoiding deep exploration of dead ends

## Solution Found

```
Grid:
  1   3   5   2   4
  6   8  10  12   7
  9  11  13  15  17
 14  16  18  20  22
 19  24  21  23  25
```

**Verification:**
- ✓ All values 1-25 used exactly once
- ✓ Center cell (3,3) = 13
- ✓ C1: No orthogonal consecutive pairs
- ✓ C2: No diagonal pairs with difference of 2
- ✓ C3: Sum of prime positions = 126 (even)

**Prime positions sum:**
- Positions: (1,2)=3, (1,4)=2, (2,1)=6, (2,3)=10, (3,2)=11, (3,4)=15, (4,1)=14, (4,3)=18, (5,2)=24, (5,4)=23
- Sum = 3+2+6+10+11+15+14+18+24+23 = 126 ✓

## Complexity Analysis

- **Time Complexity**: O(24! × constraint_checks) in worst case, but significantly reduced by:
  - Early pruning of invalid branches
  - Constraint propagation
  - Early C3 validation
  
- **Space Complexity**: O(25) for the grid and used set

## Alternative Approaches Considered

1. **Constraint Programming (CP)**: Could use libraries like `python-constraint`, but custom backtracking gives more control
2. **SAT Solving**: Could encode as a SAT problem, but the encoding would be complex
3. **Genetic Algorithms**: Might work but doesn't guarantee finding a solution
4. **Heuristic Search**: Could use domain-specific heuristics, but backtracking is more reliable

## Conclusion

The backtracking approach successfully finds a solution by:
- Systematically exploring the search space
- Pruning invalid branches early
- Validating constraints incrementally
- Ensuring all constraints are satisfied before accepting a solution

The solution demonstrates that despite the highly restrictive constraints, a valid assignment exists and can be found algorithmically.
