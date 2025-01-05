from collections.abc import Generator
from heapq import heappop, heappush
from itertools import pairwise
from typing import Literal

import pytest

from utils import no_input_skip, read_input

KeypadKeys = Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A"]
DirectionKeys = Literal["<", ">", "^", "v", "A"]
Point = tuple[int, int]
Keypad = dict[KeypadKeys, Point] | dict[DirectionKeys, Point]

# fmt: off
numeric_keypad: dict[Point, KeypadKeys] = {
    (0, 0): '7', (1, 0): '8', (2, 0): '9',
    (0, 1): '4', (1, 1): '5', (2, 1): '6',
    (0, 2): '1', (1, 2): '2', (2, 2): '3',
    (1, 3): '0', (2, 3): 'A'
}
# fmt: on
numeric_keypad_reversed: dict[KeypadKeys, Point] = {v: k for k, v in numeric_keypad.items()}

# fmt: off
directional_keypad: dict[Point, DirectionKeys] = {
    (1, 0): '^', (2, 0): 'A',
    (0, 1): '<', (1, 1): 'v', (2, 1): '>'
}
# fmt: on
directional_keypad_reversed: dict[DirectionKeys, Point] = {v: k for k, v in directional_keypad.items()}

directions = [
    (-1, 0, "<", 1),
    (0, -1, "^", 2),
    (0, 1, "v", 3),
    (1, 0, ">", 4),
]


def find_paths(start: Point, end: Point, keypad: Keypad) -> Generator[str, None, None]:
    queue: list[tuple[int, int, int, str, set[Point]]] = []
    heappush(queue, (0, start[0], start[1], "", {start}))

    while queue:
        dist, x, y, path, visited = heappop(queue)

        if (x, y) == end:
            yield path + "A"

        for dir_x, dir_y, move, _ in directions:
            new_x, new_y = x + dir_x, y + dir_y
            if (new_x, new_y) in keypad.values() and (new_x, new_y) not in visited:
                score = 1 if move == (path or "n")[-1] else 10
                heappush(queue, (dist + score, new_x, new_y, path + move, {*visited, (new_x, new_y)}))


def get_path_between(start: str, end: str, keypad: Keypad, keypad_count: int) -> str:
    if not keypad_count:
        return "A"

    paths = []
    shortest_path = "A" * 99999
    for path in find_paths(keypad[start], keypad[end], keypad):
        got_path = get_path(directional_keypad_reversed, path, keypad_count - 1)
        paths.append(got_path)
        if len(got_path) < len(shortest_path):
            shortest_path = got_path
    return shortest_path


def get_path(keypad: Keypad, code: str, keypad_count: int) -> str:
    path = ""
    for a, b in pairwise("A" + code):
        path += get_path_between(a, b, keypad, keypad_count)
    return path


def get_move_list(code: str) -> str:
    return get_path(numeric_keypad_reversed, code, 3)


def part_1(puzzle: str) -> int:
    codes = puzzle.splitlines()
    total_complexity = 0

    for code in codes:
        moves = get_path(numeric_keypad_reversed, code, 3)
        total_complexity += len(moves) * int(code[:-1])

    return total_complexity


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """029A
980A
179A
456A
379A"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 126384


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("029A", 68),
        ("980A", 60),
        ("179A", 68),
        ("456A", 64),
        ("379A", 64),
    ],
)
def test_single_code(test_input, expected):
    moves = get_move_list(test_input)

    assert len(moves) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("382A", 68),
        ("176A", 74),
        ("463A", 70),
        ("083A", 66),
        ("789A", 66),
    ],
)
def test_real_single_code(test_input, expected):
    moves = get_move_list(test_input)

    assert len(moves) == expected


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 128962


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
