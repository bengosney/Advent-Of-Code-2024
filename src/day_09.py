from typing import Literal

import pytest
from rich.progress import Progress

from utils import no_input_skip, read_input

Block = int | Literal["."]


def parse_input(puzzle: str) -> list[Block]:
    blocks: list[Block] = []
    current_id = 0
    is_file = True
    for size in puzzle.strip():
        value: Block = current_id if is_file else "."
        blocks.extend([value for _ in range(int(size))])
        if is_file:
            current_id += 1
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


def sort_files(blocks: list[Block]) -> list[Block]:
    right = len(blocks) - 1
    moved: set[int] = set()
    first_space = 0

    with Progress(transient=True) as progress:
        task = progress.add_task("Sorting files...", total=right)
        total = right
        while right >= 0:
            progress.update(task, completed=total - right)
            while right >= 0 and (blocks[right] == "." and blocks[right] not in moved):
                right -= 1
            f2 = right
            while right >= 0 and blocks[right] == blocks[f2]:
                right -= 1
            length = f2 - right
            f1 = right + 1
            f2 = f1 + length

            space_found = 0
            set_first_space = False
            for i in range(first_space, f1):
                if blocks[i] == ".":
                    space_found += 1
                    if not set_first_space:
                        first_space = i
                        set_first_space = True
                else:
                    space_found = 0
                if space_found == length:
                    break
            else:
                continue

            s2 = i + 1
            s1 = s2 - length
            blocks[s1:s2], blocks[f1:f2] = blocks[f1:f2], blocks[s1:s2]

    return blocks


def checksum(blocks: list[Block]) -> int:
    return sum(position * int(id) for position, id in enumerate(blocks) if id != ".")


def part_1(puzzle: str) -> int:
    blocks = parse_input(puzzle)
    blocks = sort_blocks(blocks)

    return checksum(blocks)


def part_2(puzzle: str) -> int:
    blocks = parse_input(puzzle)
    blocks = sort_files(blocks)

    return checksum(blocks)


# -- Tests


def get_example_input() -> str:
    return "2333133121414131402"


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 1928


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 2858


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 6258319840548


@no_input_skip
@pytest.mark.slow
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 6286182965311


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
