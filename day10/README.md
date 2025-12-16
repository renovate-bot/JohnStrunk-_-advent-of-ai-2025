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

### Part 2: Integer Linear Programming (ILP)

The joltage counter problem is a classic Integer Linear Programming
optimization problem:

**Problem Formulation:**

- **Variables:** x₁, x₂, ..., xₘ (number of times to press each button)
- **Objective:** Minimize Σxᵢ (total button presses)
- **Constraints:**
  - For each counter j: Σ(xᵢ where button i affects counter j) = target[j]
  - All xᵢ ≥ 0 and integer

**Algorithm:**

1. Build coefficient matrix A where `A[counter][button] = 1` if that button
   affects that counter
2. Create ILP problem with:
   - Decision variables for each button (non-negative integers)
   - Objective: minimize sum of all button press variables
   - Constraints: sum of button presses affecting each counter = target value
3. Solve using CBC (COIN-OR Branch and Cut) solver via PuLP library
4. Extract optimal solution

**Time Complexity:** Polynomial in practice for most instances, though ILP is
NP-hard in the worst case. The CBC solver uses branch-and-bound with cutting
planes, making it very efficient for typical problem sizes.

**Why ILP Instead of Search:**

Search-based approaches (BFS, DFS, A*) fail on this problem because the state
space is too large. For targets like `[198, 181, 22, 50, 173, 65]`, there are
billions of possible states even with aggressive pruning.

ILP solvers are specifically designed for this type of optimization and handle
it efficiently by:

- Using LP relaxation to compute bounds
- Pruning the search tree intelligently
- Applying cutting plane algorithms to tighten constraints

## Challenges

1. **Part 1:** Handling underdetermined systems where multiple solutions
   exist, requiring enumeration over free variables.

2. **Part 2:** Initial attempts using search-based algorithms (BFS, DFS, A*)
   failed due to the enormous state space. With targets up to 257, even with
   aggressive pruning, the number of reachable states can be in the billions.
   The solution required recognizing this as an optimization problem and using
   Integer Linear Programming.

3. **Algorithm Selection:** This problem demonstrates the importance of
   choosing the right algorithm. Search algorithms are intuitive but infeasible
   for large state spaces. ILP, while more complex to set up, solves the
   problem optimally in under a second by exploiting the mathematical structure
   of the constraints.
