from collections import defaultdict
from itertools import combinations

import pytest

from utils import no_input_skip, read_input


def parse_input(puzzle: str) -> list[tuple[int, int]]:
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

    return [(int(p.real), int(p.imag)) for p in path]


def count_cheets(path: list[tuple[int, int]], max_skip: int, min_skip: int) -> dict[int, int]:
    cheats = defaultdict(int)
    index_map = {point: index for index, point in enumerate(path)}
    for a, b in combinations(path, 2):
        if (steps := (index_map[b] - index_map[a])) >= min_skip:
            if (distance := abs(a[0] - b[0]) + abs(a[1] - b[1])) <= max_skip:
                diff = steps - distance
                if diff > 0:
                    cheats[diff] += 1

    return cheats


def part_1(puzzle: str) -> int:
    path = parse_input(puzzle)
    cheats = count_cheets(path, 2, 100)

    return sum(count for saving, count in cheats.items() if saving >= 100)


def part_2(puzzle: str) -> int:
    path = parse_input(puzzle)
    cheats = count_cheets(path, 20, 100)

    return sum(count for saving, count in cheats.items() if saving >= 100)


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
    cheats = count_cheets(path, 2, 1)
    assert cheats == output


def test_part_2() -> None:
    test_input = get_example_input()
    output = {
        50: 32,
        52: 31,
        54: 29,
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    }
    path = parse_input(test_input)
    cheats = count_cheets(path, 20, 50)
    over_50 = {saving: count for saving, count in cheats.items() if saving >= 50}
    assert over_50 == output


@no_input_skip
@pytest.mark.slow
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 1369


@no_input_skip
@pytest.mark.slow
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 979012


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
