from collections import defaultdict
from heapq import heappop, heappush

import pytest

from utils import no_input_skip, read_input

Point = tuple[int, int]


def parse_input(puzzle: str) -> tuple[set[Point], Point, Point]:
    walls = set()

    for y, line in enumerate(puzzle.split("\n")):
        for x, cell in enumerate(line):
            if cell == "#":
                walls.add((x, y))
            elif cell == "S":
                start = (x, y)
            elif cell == "E":
                end = (x, y)
    return walls, start, end


def solve_maze(walls: set[Point], start: Point, end: Point) -> tuple[int, int]:
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    queue: list[tuple[int, int, int, int, int, set[tuple[int, int]]]] = []
    heappush(queue, (0, start[0], start[1], 1, 0, set()))

    best_score: int = 9_999_999
    scores_history: dict[int, set[Point]] = defaultdict(set)
    visited: dict[tuple[Point, Point], int] = {}

    while queue:
        score, x, y, dx, dy, history = heappop(queue)
        current_direction = (dx, dy)
        pos = (x, y)

        if score > best_score:
            continue
        if (pos, current_direction) in visited and visited[(pos, current_direction)] < score:
            continue

        visited[(pos, current_direction)] = score

        if pos == end:
            best_score = min(best_score, score)
            scores_history[score] |= history

        for next_direction in directions:
            next_pos = (x + next_direction[0], y + next_direction[1])
            if next_pos in history or next_pos in walls or next_pos in visited:
                continue

            next_score = score + 1
            if next_direction != current_direction:
                next_score += 1000

            heappush(
                queue,
                (
                    next_score,
                    next_pos[0],
                    next_pos[1],
                    next_direction[0],
                    next_direction[1],
                    history | {pos},
                ),
            )

    return best_score, len(scores_history[best_score]) + 1


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
