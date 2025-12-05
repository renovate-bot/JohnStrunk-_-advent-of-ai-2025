"""Unit tests for is_invalid_id and count_invalid_ids_in_range from part2 (Day 2 Part 2)."""

from day02.part2 import count_invalid_ids_in_range, is_invalid_id


def test_is_invalid_id_examples():
    """Test is_invalid_id for Day 2 Part 2 rules using examples from the puzzle description."""
    assert is_invalid_id(12341234) is True
    assert is_invalid_id(123123123) is True
    assert is_invalid_id(1212121212) is True
    assert is_invalid_id(1111111) is True
    assert is_invalid_id(11) is True
    assert is_invalid_id(22) is True
    assert is_invalid_id(99) is True
    assert is_invalid_id(111) is True
    assert is_invalid_id(999) is True
    assert is_invalid_id(1010) is True
    assert is_invalid_id(1188511885) is True
    assert is_invalid_id(222222) is True
    assert is_invalid_id(1698522) is False
    assert is_invalid_id(446446) is True
    assert is_invalid_id(38593859) is True
    assert is_invalid_id(565656) is True
    assert is_invalid_id(824824824) is True
    assert is_invalid_id(2121212121) is True
    assert is_invalid_id(38593856) is False
    assert is_invalid_id(565653) is False
    assert is_invalid_id(824824821) is False
    assert is_invalid_id(2121212118) is False


def test_count_invalid_ids_in_range():
    """Test count_invalid_ids_in_range for Day 2 Part 2 rules using examples from the puzzle description."""
    INVALID_11_22 = 11 + 22
    INVALID_95_115 = 99 + 111
    INVALID_998_1012 = 999 + 1010
    INVALID_1188511880_1188511890 = 1188511885
    INVALID_222220_222224 = 222222
    INVALID_1698522_1698528 = 0
    INVALID_446443_446449 = 446446
    INVALID_38593856_38593862 = 38593859
    INVALID_565653_565659 = 565656
    INVALID_824824821_824824827 = 824824824
    INVALID_2121212118_2121212124 = 2121212121

    assert count_invalid_ids_in_range(11, 22) == INVALID_11_22
    assert count_invalid_ids_in_range(95, 115) == INVALID_95_115
    assert count_invalid_ids_in_range(998, 1012) == INVALID_998_1012
    assert (
        count_invalid_ids_in_range(1188511880, 1188511890)
        == INVALID_1188511880_1188511890
    )
    assert count_invalid_ids_in_range(222220, 222224) == INVALID_222220_222224
    assert count_invalid_ids_in_range(1698522, 1698528) == INVALID_1698522_1698528
    assert count_invalid_ids_in_range(446443, 446449) == INVALID_446443_446449
    assert count_invalid_ids_in_range(38593856, 38593862) == INVALID_38593856_38593862
    assert count_invalid_ids_in_range(565653, 565659) == INVALID_565653_565659
    assert (
        count_invalid_ids_in_range(824824821, 824824827) == INVALID_824824821_824824827
    )
    assert (
        count_invalid_ids_in_range(2121212118, 2121212124)
        == INVALID_2121212118_2121212124
    )
