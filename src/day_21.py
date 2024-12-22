from collections import deque
from typing import Literal, Self, cast

import pytest

from utils import NoSolutionError, no_input_skip, read_input  # noqa: F401

KeypadKeys = Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A"]
DirectionKeys = Literal["<", ">", "^", "v", "A"]


class Keypad:
    # fmt: off
    key_map: dict[KeypadKeys | None, tuple[int, int]] = {  # noqa: RUF012
        "7": (0, 0), "8": (1, 0), "9": (2, 0),
        "4": (0, 1), "5": (1, 1), "6": (2, 1),
        "1": (0, 2), "2": (1, 2), "3": (2, 2),
                     "0": (1, 3), "A": (2, 3),
    }
    # fmt: on

    def __init__(self) -> None:
        print("init keypad")
        self.x, self.y = self.key_map["A"]

    def press_key(self, key: KeypadKeys) -> list[list[DirectionKeys]]:
        end_x, end_y = self.key_map[key]
        queue: deque[tuple[int, int, int, list[DirectionKeys]]] = deque()
        visited: set[tuple[int, int]] = set()
        valid_positions: set[tuple[int, int]] = set(self.key_map.values())
        neighbours: list[tuple[DirectionKeys, int, int]] = [
            ("v", 0, 1),
            ("^", 0, -1),
            (">", 1, 0),
            ("<", -1, 0),
        ]

        paths = []

        queue.append((0, self.x, self.y, []))
        while queue:
            dist, x, y, history = queue.popleft()
            if (x, y) == (end_x, end_y):
                self.x, self.y = end_x, end_y
                print("-")
                print(f"Keypad {key}: {[*history, "A"]}")
                paths.append([*history, "A"])
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dir, d_x, d_y in neighbours:
                next_x = x + d_x
                next_y = y + d_y
                if (next_x, next_y) in valid_positions:
                    try:
                        score = DirectionPad.move_cost(history[-1], dir)
                    except IndexError:
                        score = DirectionPad.move_cost("A", dir)
                    queue.append((dist + score, next_x, next_y, [*history, dir]))

        return paths


class DirectionPad:
    # fmt: off
    key_map: dict[DirectionKeys | None, tuple[int, int]] = {  # noqa: RUF012
                      "^": (1, 0), "A": (2, 0),
         "<": (0, 1), "v": (1, 1), ">": (2, 1),
    }
    # fmt: on

    def __init__(self, pad: Self | Keypad, cost: bool) -> None:
        print("init direction pad")
        self.next_pad = pad
        self.x, self.y = self.key_map["A"]
        self.cost = cost

    def press_key(self, key: KeypadKeys) -> list[list[DirectionKeys]]:
        moves = self.next_pad.press_key(key)
        my_moves = []
        for move in moves:
            my_moves.extend(self.move_to(move))

        return my_moves

    def move_to(self, key: DirectionKeys) -> list[list[DirectionKeys]]:
        end_x, end_y = self.key_map[key]
        queue: deque[tuple[int, int, int, list[DirectionKeys]]] = deque()
        visited: set[tuple[int, int]] = set()
        valid_positions: set[tuple[int, int]] = set(self.key_map.values())
        neighbours: list[tuple[DirectionKeys, int, int]] = [
            ("<", -1, 0),
            (">", 1, 0),
            ("v", 0, 1),
            ("^", 0, -1),
        ]

        paths = []

        queue.append((0, self.x, self.y, []))
        while queue:
            dist, x, y, history = queue.popleft()
            if (x, y) == (end_x, end_y):
                self.x, self.y = end_x, end_y
                if self.cost:
                    print(f"DirPad {key}: {[*history, 'A']} {dist}")
                else:
                    print(f"MeePad {key}: {[*history, 'A']} {dist}")
                paths.append([*history, "A"])
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dir, d_x, d_y in neighbours:
                next_x = x + d_x
                next_y = y + d_y
                if (next_x, next_y) in valid_positions:
                    if self.cost:
                        try:
                            score = DirectionPad.move_cost(history[-1], dir)
                        except IndexError:
                            score = DirectionPad.move_cost("A", dir)
                    else:
                        score = 1
                    queue.append((dist + score, next_x, next_y, [*history, dir]))

        return paths

    @staticmethod
    def move_cost(start: DirectionKeys, end: DirectionKeys) -> int:
        a = DirectionPad.key_map[start]
        b = DirectionPad.key_map[end]
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


def parse_input(puzzle: str) -> list[list[str]]:
    return list(map(list, puzzle.splitlines()))


def init_chain() -> DirectionPad:
    print("init chain")
    keypad = Keypad()
    direction_pad_1 = DirectionPad(keypad, True)
    direction_pad_2 = DirectionPad(direction_pad_1, False)
    return direction_pad_2


def part_1(puzzle: str) -> int:
    codes = parse_input(puzzle)

    complexities = []
    for code in codes:
        direction_pad = init_chain()
        all_moves = 0
        for key in code:
            moves = direction_pad.press_key(cast(KeypadKeys, key))
            all_moves += len(moves)

        print(f"{"".join(code)}: {all_moves} * {int("".join(code[:-1]))}")
        complexities.append(all_moves * int("".join(code[:-1])))

    return sum(complexities)


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
    direction_pad = init_chain()
    total = 0
    all_moves = []
    for c in test_input:
        moves = direction_pad.press_key(c)
        all_moves.extend(moves)
        all_moves.append("|")
        total += len(moves)

    print(f"{test_input}: {''.join(all_moves)}")
    print("    : <v<A>>^AvA^A|<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")
    assert total == expected


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
    keypad = Keypad()
    moves = []
    for key in "029A":
        moves.extend(keypad.press_key(key))
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
