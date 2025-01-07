from collections.abc import Iterable
from itertools import pairwise

from utils import no_input_skip, read_input


def check_row(row: Iterable[int]) -> bool:
    row_dir = 0
    for a, b in pairwise(row):
        direction = (a < b) - (a > b)
        if abs(a - b) not in (1, 2, 3) or row_dir not in (0, direction):
            return False
        row_dir = direction

    return True


def puzzle_to_ints(puzzle: str) -> list[list[int]]:
    return [list(map(int, row.split())) for row in puzzle.splitlines()]


def part_1(puzzle: str) -> int:
    return sum(check_row(row) for row in puzzle_to_ints(puzzle))


def part_2(puzzle: str) -> int:
    return sum(
        check_row(row) or any(check_row(row[:i] + row[i + 1 :]) for i in range(len(row)))
        for row in puzzle_to_ints(puzzle)
    )


# -- Tests


def get_example_input() -> str:
    return """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 2


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 4


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 432


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 488


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
