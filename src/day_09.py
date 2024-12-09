from typing import Literal

from utils import no_input_skip, read_input

Block = int | Literal["."]


def parse_input(puzzle: str) -> list[Block]:
    blocks = []
    id = 0
    is_file = True
    for size in puzzle.strip():
        value = id if is_file else "."
        blocks.extend([value] * int(size))
        if is_file:
            id += 1
        is_file = not is_file

    return blocks


def sort_blocks(blocks: list[Block]) -> list[Block]:
    blocks = blocks.copy()
    left, right = 0, len(blocks) - 1

    while left < right:
        while left < right and blocks[left] != ".":
            left += 1
        while left < right and blocks[right] == ".":
            right -= 1
        if left < right:
            blocks[left], blocks[right] = blocks[right], blocks[left]
            left += 1
            right -= 1

    return blocks


def checksum(blocks: list[Block]) -> int:
    value = 0
    for position, id in enumerate(blocks):
        if id == ".":
            continue

        value += position * int(id)

    return value


def part_1(puzzle: str) -> int:
    blocks = parse_input(puzzle)
    blocks = sort_blocks(blocks)

    return checksum(blocks)


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def test_sort_blocks() -> None:
    input = parse_input(get_example_input())
    result = sort_blocks(input)
    assert result == [
        0,
        0,
        9,
        9,
        8,
        1,
        1,
        1,
        8,
        8,
        8,
        2,
        7,
        7,
        7,
        3,
        3,
        3,
        6,
        4,
        4,
        6,
        5,
        5,
        5,
        5,
        6,
        6,
        *list(".............."),
    ]


def get_example_input() -> str:
    return "2333133121414131402"


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 1928


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 6258319840548


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
