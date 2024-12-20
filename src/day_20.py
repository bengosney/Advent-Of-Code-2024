from collections import defaultdict
from itertools import combinations

import pytest

from utils import no_input_skip, read_input


def parse_input(puzzle: str) -> list[complex]:
    track: set[complex] = set()
    start = complex(0, 0)
    end = complex(0, 0)
    for y, line in enumerate(puzzle.split("\n")):
        for x, char in enumerate(line):
            if char != "#":
                track.add(complex(x, y))
            if char == "S":
                start = complex(x, y)
            if char == "E":
                end = complex(x, y)

    path = [start]
    while path[-1] != end:
        for step in [path[-1] + 1j, path[-1] - 1j, path[-1] + 1, path[-1] - 1]:
            if step in track and step not in path:
                path.append(step)
                break

    return path


def manhattan_distance(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def count_cheets(path: list[complex]) -> dict[int, int]:
    cheats = defaultdict(int)
    for a, b in combinations(path, 2):
        if manhattan_distance(a, b) <= 2:
            a_index = path.index(a)
            b_index = path.index(b)
            diff = (b_index - a_index) - 2
            if diff > 0:
                cheats[diff] += 1

    return cheats


def part_1(puzzle: str) -> int:
    path = parse_input(puzzle)
    cheats = count_cheets(path)

    return sum(count for saving, count in cheats.items() if saving >= 100)


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


def test_part_1() -> None:
    test_input = get_example_input()
    output = {2: 14, 4: 14, 6: 2, 8: 4, 10: 2, 12: 3, 20: 1, 36: 1, 38: 1, 40: 1, 64: 1}

    path = parse_input(test_input)
    cheats = count_cheets(path)
    assert cheats == output


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
@pytest.mark.slow
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 1369


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
