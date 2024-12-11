from functools import cache

from utils import no_input_skip, read_input


def parse_input(puzzle: str) -> list[int]:
    return list(map(int, puzzle.split()))


@cache
def blink(stone: int, itterations: int) -> int:
    if itterations == 0:
        return 1

    if stone == 0:
        return blink(1, itterations - 1)
    elif len(str(stone)) % 2 == 0:
        chars = str(stone)
        middle = len(chars) // 2
        return blink(int(chars[:middle]), itterations - 1) + blink(int(chars[middle:]), itterations - 1)
    else:
        return blink(stone * 2024, itterations - 1)


def part_1(puzzle: str) -> int:
    stones = parse_input(puzzle)

    total = 0
    for stone in stones:
        total += blink(stone, 25)

    return total


def part_2(puzzle: str) -> int:
    stones = parse_input(puzzle)

    total = 0
    for stone in stones:
        total += blink(stone, 75)

    return total


# -- Tests


def get_example_input() -> str:
    return "125 17"


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 55312


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 203457


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 241394363462435


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
