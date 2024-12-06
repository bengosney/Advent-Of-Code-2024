from collections import deque

import pytest
from rich.progress import Progress

from utils import no_input_skip, read_input

Point = tuple[int, int]


def puzzle_to_map(puzzle: str) -> tuple[dict[Point, str], Point]:
    map = {}
    start = (-1, -1)
    for y, line in enumerate(puzzle.splitlines()):
        for x, cell in enumerate(line):
            if cell == "^":
                start = (x, y)
            map[(x, y)] = "." if cell == "^" else cell

    return map, start


class LoopingError(Exception):
    pass


def walk_path(map: dict[Point, str], start: Point) -> set[Point]:
    position = start
    directions = deque([(0, -1), (1, 0), (0, 1), (-1, 0)])
    seen_directions: set[tuple[Point, Point]] = set()

    try:
        while True:
            if (directions[0], position) in seen_directions:
                raise LoopingError()
            seen_directions.add((directions[0], position))
            next_position = (position[0] + directions[0][0], position[1] + directions[0][1])
            next = map[next_position]
            if next == "#":
                directions.rotate(-1)
            else:
                position = next_position
    except KeyError:
        pass

    return {p for _, p in seen_directions}


def part_1(puzzle: str) -> int:
    map, start_position = puzzle_to_map(puzzle)
    seen = walk_path(map, start_position)

    return len(seen)


def part_2(puzzle: str) -> int:
    map, start_position = puzzle_to_map(puzzle)
    seen = walk_path(map, start_position)

    loops = 0
    with Progress(transient=True) as progress:
        task = progress.add_task("Obstructions", total=len(seen))
        for obstruction_position in seen:
            progress.update(task, advance=1)
            map[obstruction_position] = "#"
            try:
                walk_path(map, start_position)
            except LoopingError:
                loops += 1
            map[obstruction_position] = "."

    return loops


# -- Tests


def test_looping_error():
    input = """....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.#^---+.
........#.
#.........
......#..."""
    map, position = puzzle_to_map(input)
    with pytest.raises(LoopingError):
        walk_path(map, position)


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


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 6


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 5404


@no_input_skip
@pytest.mark.slow
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 1984


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
