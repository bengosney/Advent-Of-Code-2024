from utils import read_input, no_input_skip  # noqa
from itertools import pairwise


def check_row(row: list[int]) -> bool:
    row_dir = 0
    for a, b in pairwise(row):
        dir = -1 if a < b else 1
        if row_dir not in (0, dir):
            return False
        row_dir = dir

        change = abs(a - b)
        if change not in (1, 2, 3):
            return False

    return True


def part_1(puzzle: str) -> int:
    ok = 0
    for row in puzzle.splitlines():
        if check_row(list(map(int, row.split()))):
            ok += 1

    return ok


def part_2(puzzle: str) -> int:
    ok = 0
    for row in puzzle.splitlines():
        values = list(map(int, row.split()))
        if check_row(values):
            ok += 1
            continue

        for i in range(0, len(values)):
            tmp = values.copy()
            del tmp[i]

            if check_row(tmp):
                ok += 1
                break

    return ok


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
