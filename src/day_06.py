from collections import deque

from utils import no_input_skip, read_input

Point = tuple[int, int]


def puzzle_to_map(puzzle: str) -> tuple[dict[Point, str], Point]:
    map = {}
    start = (-1, -1)
    for y, line in enumerate(puzzle.splitlines()):
        for x, cell in enumerate(line):
            if cell == "^":
                start = (x, y)
                map[(x, y)] = "."
            else:
                map[(x, y)] = cell

    return map, start


def add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1] + b[1])


def part_1(puzzle: str) -> int:
    map, position = puzzle_to_map(puzzle)
    directions = deque([(0, -1), (1, 0), (0, 1), (-1, 0)])

    seen: set[Point] = set()

    try:
        while True:
            seen.add(position)
            next = map[add(position, directions[0])]
            if next == "#":
                directions.rotate(-1)
            else:
                position = add(position, directions[0])
    except KeyError:
        pass

    return len(seen)


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 41


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 5404


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")