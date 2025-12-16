"""
Solution for Day 10, Part 2.

This module contains the solution for Part 2 of Day 10 using Integer Linear Programming.
"""

import pulp  # type: ignore[import-untyped]


def parse_input(input_data: str) -> list[tuple[list[int], list[tuple[int, ...]]]]:
    """
    Parse the input data into a list of machines.

    Args:
        input_data (str): The raw input data.

    Returns:
        list: A list of tuples, each containing the target joltage levels and button wiring.
    """
    machines: list[tuple[list[int], list[tuple[int, ...]]]] = []
    for line in input_data.strip().split("\n"):
        parts = line.split()
        # Extract joltage requirements (last item in {curly braces})
        joltage_str = next(p for p in reversed(parts) if p.startswith("{"))
        joltage = list(map(int, joltage_str[1:-1].split(",")))
        # Extract button wiring schematics
        buttons = [
            tuple(map(int, b[1:-1].split(","))) for b in parts if b.startswith("(")
        ]
        machines.append((joltage, buttons))
    return machines


def min_button_presses(target: list[int], buttons: list[tuple[int, ...]]) -> int:
    """
    Find minimum button presses using Integer Linear Programming.

    Args:
        target: Target joltage levels for each counter
        buttons: List of button wirings (which counters each button affects)

    Returns:
        Minimum number of button presses, or -1 if unsolvable
    """
    n = len(target)  # number of counters
    m = len(buttons)  # number of buttons

    # Create the ILP problem
    prob = pulp.LpProblem("MinButtonPresses", pulp.LpMinimize)

    # Create variables for each button (number of times to press it)
    # Each variable is a non-negative integer
    button_vars = [
        pulp.LpVariable(f"button_{i}", lowBound=0, cat="Integer") for i in range(m)
    ]

    # Objective: minimize total button presses
    prob += pulp.lpSum(button_vars)

    # Constraints: for each counter, sum of button presses must equal target
    for counter_idx in range(n):
        # Which buttons affect this counter?
        affecting_buttons = [
            button_vars[btn_idx]
            for btn_idx, button in enumerate(buttons)
            if counter_idx in button
        ]

        # Sum of those button presses must equal the target for this counter
        prob += pulp.lpSum(affecting_buttons) == target[counter_idx]

    # Solve the problem (suppress solver output)
    prob.solve(pulp.PULP_CBC_CMD(msg=False))  # type: ignore[reportUnknownMemberType]

    # Check if solution was found
    if prob.status != pulp.LpStatusOptimal:  # type: ignore[reportUnknownMemberType]
        return -1

    # Return the total number of button presses
    return int(pulp.value(prob.objective))  # type: ignore[reportUnknownMemberType, reportArgumentType]


def solve(input_data: str) -> int:
    """
    Solve the Day 10, Part 2 puzzle for all machines in the input.

    Args:
        input_data (str): The raw input data for all machines.

    Returns:
        int: The total minimum number of button presses for all machines, or -1 if any is unsolvable.
    """
    machines = parse_input(input_data)
    total_presses: int = 0
    for joltage, buttons in machines:
        presses = min_button_presses(joltage, buttons)
        if presses == -1:
            return -1
        total_presses += presses
    return total_presses


if __name__ == "__main__":
    with open("input.txt") as f:
        input_data = f.read()
    print(solve(input_data))
