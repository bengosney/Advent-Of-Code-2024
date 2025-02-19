from collections import defaultdict
from itertools import combinations

from utils import no_input_skip, read_input


def parse_input(puzzle: str) -> tuple[dict[str, set[complex]], complex]:
    puzzle_map: dict[str, set[complex]] = defaultdict(set)
    for y, line in enumerate(puzzle.splitlines()):
        for x, cell in enumerate(line):
            if cell != ".":
                puzzle_map[cell].add(complex(x, y))

    return puzzle_map, complex(x, y)


def part_1(puzzle: str) -> int:
    puzzle_map, extents = parse_input(puzzle)
    antinodes: set[complex] = set()

    def in_bounds(a: complex) -> bool:
        return 0 <= a.real <= extents.real and 0 <= a.imag <= extents.imag

    for positions in puzzle_map.values():
        for a, b in combinations(positions, 2):
            dist = a - b
            antinodes.add(a + dist)
            antinodes.add(b - dist)

    return len({a for a in antinodes if in_bounds(a)})


def part_2(puzzle: str) -> int:
    puzzle_map, extents = parse_input(puzzle)
    antinodes: set[complex] = set()

    def in_bounds(a: complex) -> bool:
        return 0 <= a.real <= extents.real and 0 <= a.imag <= extents.imag

    def calculate_nodes(start: complex, dist: complex) -> None:
        node = start
        while in_bounds(node):
            antinodes.add(node)
            node += dist

    for positions in puzzle_map.values():
        for a, b in combinations(positions, 2):
            calculate_nodes(a, a - b)
            calculate_nodes(b, b - a)

    return len(antinodes)


# -- Tests


def get_example_input() -> str:
    return """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 14


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 34


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 261


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 898


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
