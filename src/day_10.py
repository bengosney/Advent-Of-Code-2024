from collections import defaultdict, deque

from utils import no_input_skip, read_input


def parse_input(puzzle: str) -> dict[complex, int]:
    map = defaultdict(int)
    for y, line in enumerate(puzzle.splitlines()):
        for x, value in enumerate(line):
            try:
                map[complex(x, y)] = int(value)
            except ValueError:
                pass

    return map


def draw_map(map: dict[complex, str]) -> None:
    ex = int(max(map.keys(), key=lambda x: x.real).real) + 2
    ey = int(max(map.keys(), key=lambda x: x.imag).imag) + 2

    for y in range(-1, ey):
        for x in range(-1, ex):
            print(map[complex(x, y)], end="")
        print()


def walk_trail(map: dict[complex, int], starts: list[complex]) -> int:
    directions: list[complex] = [1 + 0j, 0 + 1j, -1 + 0j, 0 + -1j]
    score = 0

    for start in starts:
        steps = deque([start])
        found = set()
        while steps:
            position = steps.popleft()
            if map[position] == 9:
                found.add(position)
            else:
                for direction in directions:
                    new_position = position + direction
                    if map[new_position] - map[position] == 1:
                        steps.append(new_position)
        score += len(found)

    return score


def part_1(puzzle: str) -> int:
    map = parse_input(puzzle)

    starts = []
    for position, value in map.items():
        if value == 0:
            starts.append(position)

    return walk_trail(map, starts)


def part_2(puzzle: str) -> int:
    pass


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


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 841


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
