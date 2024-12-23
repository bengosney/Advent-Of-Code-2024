from heapq import heappop, heappush
from typing import Literal

import pytest
from icecream import ic

from utils import NoSolutionError, no_input_skip, read_input  # noqa: F401

KeypadKeys = Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A"]
DirectionKeys = Literal["<", ">", "^", "v", "A"]
Point = tuple[int, int]
Keypad = dict[Point, KeypadKeys] | dict[Point, DirectionKeys]

# fmt: off
numeric_keypad: dict[Point, KeypadKeys] = {
    (0, 0): '7', (1, 0): '8', (2, 0): '9',
    (0, 1): '4', (1, 1): '5', (2, 1): '6',
    (0, 2): '1', (1, 2): '2', (2, 2): '3',
    (1, 3): '0', (2, 3): 'A'
}
# fmt: on
numeric_keypad_reversed = {v: k for k, v in numeric_keypad.items()}
ic(numeric_keypad_reversed)

# fmt: off
directional_keypad: dict[Point, DirectionKeys] = {
    (1, 0): '^', (2, 0): 'A',
    (0, 1): '<', (1, 1): 'v', (2, 1): '>'
}
# fmt: on
directional_keypad_reversed = {v: k for k, v in directional_keypad.items()}

directions = [
    (0, -1, "^"),
    (0, 1, "v"),
    (-1, 0, "<"),
    (1, 0, ">"),
]


def score_move(start: Point, end: Point) -> int:
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def find_path(start: Point, end: Point, keypad: Keypad):
    queue = []
    heappush(queue, (0, start[0], start[1], ""))
    visited = {start}

    while queue:
        dist, x, y, path = heappop(queue)

        if (x, y) == end:
            return path

        for dx, dy, move in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in keypad and (nx, ny) not in visited:
                try:
                    score = 1 if move == path[-1] else 2
                except IndexError:
                    score = 1
                heappush(queue, (dist + score, nx, ny, path + move))
                visited.add((nx, ny))
    raise NoSolutionError()


def get_code_path(code: str) -> str:
    current_pos = numeric_keypad_reversed["A"]
    path = ""
    for digit in code:
        target_pos = numeric_keypad_reversed[digit]
        path += find_path(current_pos, target_pos, numeric_keypad) + "A"
        current_pos = target_pos
    return path


def get_directional_path(code_path: str) -> str:
    current_pos = (2, 0)
    path = ""
    for move in code_path:
        target_pos = directional_keypad_reversed[move]
        path += find_path(current_pos, target_pos, directional_keypad) + "A"
        current_pos = target_pos
    return path


def get_move_list(code: str) -> str:
    numeric_path = get_code_path(code)
    directional_path_1 = get_directional_path(numeric_path)
    directional_path_2 = get_directional_path(directional_path_1)
    return directional_path_2


def part_1(puzzle: str) -> int:
    codes = puzzle.splitlines()
    total_complexity = 0

    for code in codes:
        moves = get_move_list(code)
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


# def test_379A():
#     direction_pad = init_chain()
#     test_input = "379A"
#     total = 0
#     all_moves = []
#     for c in test_input:
#         moves = direction_pad.press_key(c)
#         all_moves.extend(moves)
#         total += len(moves)
#
#     assert "".join(all_moves) == "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"


def test_keypad() -> None:
    moves = get_code_path("029A")
    assert "".join(moves) in ["<A^A>^^AvvvA", "<A^A^>^AvvvA", "<A^A^^>AvvvA"]


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


# @no_input_skip
# def test_part_1_real() -> None:
#     real_input = read_input(__file__)
#     assert part_1(real_input) is not None


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
