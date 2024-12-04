from collections import defaultdict

from utils import no_input_skip, read_input

WORD_TO_FIND = "XMAS"
WORD_LENGTH = len(WORD_TO_FIND)


def puzzle_to_grid(puzzle: str) -> dict:
    grid = defaultdict(str)
    lines = puzzle.split("\n")

    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            grid[(x, y)] = cell

    return grid


def part_1(puzzle: str) -> int:
    grid = puzzle_to_grid(puzzle)

    to_check = [list(WORD_TO_FIND), list(reversed(WORD_TO_FIND))]
    found = 0

    for x, y in [k for k in grid.keys()]:
        if [grid[(x + i, y)] for i in range(WORD_LENGTH)] in to_check:
            found += 1

        if [grid[(x, y + i)] for i in range(WORD_LENGTH)] in to_check:
            found += 1

        if [grid[(x + i, y + i)] for i in range(WORD_LENGTH)] in to_check:
            found += 1

        if [grid[(x - i, y + i)] for i in range(WORD_LENGTH)] in to_check:
            found += 1

    return found


def part_2(puzzle: str) -> int:
    grid = puzzle_to_grid(puzzle)

    found = 0

    to_check = [
        ["M", "S", "A", "M", "S"],
        ["S", "M", "A", "S", "M"],
        ["M", "S", "A", "M", "s"],
        ["S", "S", "A", "M", "M"],
        ["M", "M", "A", "S", "S"],
    ]

    for x, y in [k for k in grid.keys()]:
        if [grid[(x, y)], grid[(x + 2, y)], grid[(x + 1, y + 1)], grid[(x, y + 2)], grid[(x + 2, y + 2)]] in to_check:
            found += 1

    return found


# -- Tests


def get_example_input() -> str:
    return """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 18


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 9


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 2567


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 2029


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
