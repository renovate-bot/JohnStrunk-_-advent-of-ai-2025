# Day 10: Factory

## Problem Description

### Part 1: Indicator Lights

The task is to configure indicator lights on factory machines. Each machine
has:

- A set of indicator lights (initially all off)
- A target configuration showing which lights should be on/off
- Buttons that toggle specific lights

The goal is to find the minimum number of button presses needed to configure
all machines.

### Part 2: Joltage Counters

Instead of toggling lights, the machines now have joltage counters (initially
all at 0). Each button increments specific counters by 1. The goal is to find
the minimum number of button presses to reach the target joltage levels for
all machines.

## Solution

### Part 1: Gaussian Elimination over GF(2)

The indicator light problem is a system of linear equations over GF(2)
(the binary field):

- Each button press is a binary variable (pressed or not pressed)
- Light states are binary (on or off)
- Operations are XOR (toggle)

**Algorithm:**

1. Build coefficient matrix A where `A[i][j] = 1` if button j affects light i
2. Perform Gaussian elimination over GF(2) to find the solution space
3. Identify free variables (buttons that can be pressed any number of times)
4. Try all combinations of free variables (0 or 1) to find the minimum total
   presses
5. Use back-substitution to solve for dependent variables

**Time Complexity:** O(n³ + 2^f × m) where n is the number of lights, m is
the number of buttons, and f is the number of free variables.

**Key Optimizations:**

- Using NamedTuple for back_substitute parameters to reduce memory allocations
- Efficient pivot finding
- Early inconsistency detection

### Part 2: Gaussian Elimination over Integers

The joltage counter problem is a system of linear equations over
non-negative integers:

- Each button can be pressed multiple times (non-negative integer)
- Counter values are non-negative integers
- Operations are addition

**Algorithm:**

1. Build coefficient matrix A where `A[i][j] = 1` if button j affects counter i
2. Perform Gaussian elimination using rational arithmetic (fractions) to find
   exact solutions
3. Identify free variables (buttons whose press count isn't determined by
   pivots)
4. Search over reasonable ranges of free variable values
5. For each combination, back-substitute to find dependent variables
6. Check if all variables are non-negative integers
7. Track the minimum total presses

**Time Complexity:** O(n³ + R^f × m) where n is the number of counters, m is
the number of buttons, f is the number of free variables, and R is the search
range for each free variable.

**Key Differences from Part 1:**

- Uses rational arithmetic (Fraction) instead of binary arithmetic
- Free variables can take values in `[0, max_target]` instead of just `{0, 1}`
- Must validate that solutions are non-negative integers
- Search space is much larger when there are free variables

**Optimizations:**

- Using Python's built-in Fraction for exact rational arithmetic
- Bounded search range based on maximum target value
- Early validation of solution feasibility

## Challenges

1. **Part 1:** Handling underdetermined systems where multiple solutions
   exist, requiring enumeration over free variables.

2. **Part 2:** The main challenge is determining an appropriate search range
   for free variables. The current implementation uses `max_target + 1`, which
   works for the given examples but may need adjustment for edge cases where
   buttons have overlapping effects or the optimal solution uses larger
   intermediate values.

3. **Performance:** For problems with many free variables, the search space
   grows exponentially. The current implementation is efficient for the given
   constraints but could be optimized further using techniques like:
   - Linear programming with simplex method
   - Branch and bound
   - Heuristic search strategies
