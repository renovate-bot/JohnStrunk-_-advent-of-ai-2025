# Day 6 Solution

## Approach

### Part 1

The worksheet is a grid where each problem is a vertical group of columns,
separated by a full column of spaces. Each problem's numbers are stacked
vertically, and the operator is at the bottom. For each problem, the numbers
are read as whole numbers, and the operator is applied to them. The grand total
is the sum of all problem results.

### Part 2

The worksheet is interpreted differently: each column is a digit, with the most
significant digit at the top and the least significant at the bottom. Each
number in a problem is assembled by reading its digits from top to bottom in a
single column. The operator is still at the bottom. The problems are solved as
before, but with the new digit assembly rule.

## Challenges

- Parsing the input required careful handling of columns and spaces to correctly
- identify problem boundaries.
- For part 2, assembling numbers from columns (rather than rows) was tricky and
- required a different parsing approach.
- Ensuring the solution worked for both the example and the real input required
- robust test cases and careful validation.
