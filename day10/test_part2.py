"""Tests for Day 10, Part 2."""

from day10.part2 import min_button_presses, parse_input, solve


def test_example_machines() -> None:
    """Test with the example machines from the puzzle."""
    test_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    assert solve(test_input) == 33


def test_individual_machines() -> None:
    """Test each machine individually."""
    # First machine: {3,5,4,7} with 6 buttons, expects 10 presses
    machines = parse_input("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}")
    joltage, buttons = machines[0]
    assert min_button_presses(joltage, buttons) == 10

    # Second machine: {7,5,12,7,2} with 5 buttons, expects 12 presses
    machines = parse_input(
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
    )
    joltage, buttons = machines[0]
    assert min_button_presses(joltage, buttons) == 12

    # Third machine: {10,11,11,5,10,5} with 4 buttons, expects 11 presses
    machines = parse_input(
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
    )
    joltage, buttons = machines[0]
    assert min_button_presses(joltage, buttons) == 11


def test_parse_input() -> None:
    """Test input parsing."""
    test_input = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
    machines = parse_input(test_input)

    assert len(machines) == 1
    joltage, buttons = machines[0]
    assert joltage == [3, 5, 4, 7]
    assert buttons == [(3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1)]
