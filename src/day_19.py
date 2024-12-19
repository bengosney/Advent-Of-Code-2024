from functools import cache

from utils import no_input_skip, read_input


def parse_input(puzzle: str) -> tuple[set[str], list[str]]:
    towels, patterns = puzzle.split("\n\n")

    return set(towels.split(", ")), patterns.split("\n")


def solve_pattern(towels: set[str], pattern: str) -> bool:
    @cache
    def solve(pattern: str) -> bool:
        for towel in towels:
            if pattern.startswith(towel):
                if len(towel) == len(pattern):
                    return True
                if solve(pattern[len(towel) :]):
                    return True

        return False

    return solve(pattern)


def part_1(puzzle: str) -> int:
    towels, patterns = parse_input(puzzle)

    return sum(1 for pattern in patterns if solve_pattern(towels, pattern))


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 6


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 293


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
