from collections import defaultdict, deque
from functools import partial

from utils import no_input_skip, read_input


def parse_input(puzzle: str) -> tuple[dict[complex, int], set[complex]]:
    trail_map: dict[complex, int] = defaultdict(int)
    starts: set[complex] = set()

    for y, line in enumerate(puzzle.splitlines()):
        for x, value in enumerate(line):
            trail_map[complex(x, y)] = int(value)
            if value == "0":
                starts.add(complex(x, y))

    return trail_map, starts


def walk_trail(trail_map: dict[complex, int], start: complex) -> int:
    steps = deque([start])
    found = set()
    while steps:
        position = steps.popleft()
        if trail_map[position] == 9:
            found.add(position)
        else:
            for direction in [1 + 0j, 0 + 1j, -1 + 0j, 0 + -1j]:
                if trail_map[new_position := position + direction] - trail_map[position] == 1:
                    steps.append(new_position)

    return len(found)


def part_1(puzzle: str) -> int:
    trail_map, starts = parse_input(puzzle)
    walk_trail_map = partial(walk_trail, trail_map)

    return sum(map(walk_trail_map, starts))


def count_trails(trail_map: dict[complex, int], position: complex) -> int:
    score = 0

    if trail_map[position] == 9:
        return 1

    for direction in [1 + 0j, 0 + 1j, -1 + 0j, 0 + -1j]:
        if trail_map[next_position := position + direction] - trail_map[position] == 1:
            score += count_trails(trail_map, next_position)

    return score


def part_2(puzzle: str) -> int:
    trail_map, starts = parse_input(puzzle)
    count_trails_map = partial(count_trails, trail_map)

    return sum(map(count_trails_map, starts))


# -- Tests


def get_example_input() -> str:
    return """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 36


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 81


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 841


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 1875


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
