from collections import defaultdict
from heapq import heappop, heappush
from math import inf

import pytest

from utils import no_input_skip, read_input


def parse_input(puzzle: str) -> tuple[set[complex], complex, complex]:
    walls = set()

    for y, line in enumerate(puzzle.split("\n")):
        for x, cell in enumerate(line):
            if cell == "#":
                walls.add(complex(x, y))
            elif cell == "S":
                start = complex(x, y)
            elif cell == "E":
                end = complex(x, y)
    return walls, start, end


def solve_maze(walls: set[complex], start: complex, end: complex) -> tuple[int, int]:
    directions = [complex(0, -1), complex(1, 0), complex(0, 1), complex(-1, 0)]
    queue: list[tuple[int, float, float, float, float, set[complex]]] = []
    heappush(queue, (0, start.real, start.imag, 1, 0, set()))

    best_score = inf
    scores_history: dict[int, set[complex]] = defaultdict(set)
    visited: dict[tuple[complex, complex], int] = {}

    while queue:
        score, x, y, dx, dy, history = heappop(queue)
        position = complex(x, y)
        direction = complex(dx, dy)

        if score > best_score:
            continue

        visited[(position, direction)] = score

        if position == end:
            best_score = min(best_score, score)
            scores_history[score] |= history

        for next_direction in directions:
            next_position = position + next_direction
            if next_position in history or next_position in walls:
                continue

            next_score = score + 1
            if next_direction != direction:
                next_score += 1000

            if (next_position, next_direction) in visited and visited[(next_position, next_direction)] < next_score:
                continue

            heappush(
                queue,
                (
                    next_score,
                    next_position.real,
                    next_position.imag,
                    next_direction.real,
                    next_direction.imag,
                    history | {position},
                ),
            )

    return int(best_score), len(scores_history[int(best_score)]) + 1


def part_1(puzzle: str) -> int:
    walls, start, end = parse_input(puzzle)

    score, _ = solve_maze(walls, start, end)

    return score


def part_2(puzzle: str) -> int:
    walls, start, end = parse_input(puzzle)

    _, history = solve_maze(walls, start, end)

    return history


# -- Tests


def get_example_input() -> str:
    return """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 7036


def test_part_1_2() -> None:
    test_input = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
    assert part_1(test_input) == 11048


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 45


@no_input_skip
@pytest.mark.slow
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 115500


@no_input_skip
@pytest.mark.slow
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 679


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
