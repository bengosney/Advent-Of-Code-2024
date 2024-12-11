from collections import deque

from utils import no_input_skip, read_input


def parse_input(puzzle: str) -> deque[int]:
    return deque(map(int, puzzle.split()))


def blink(stones: deque[int]) -> None:
    for _ in range(0, len(stones)):
        if stones[0] == 0:
            stones[0] = 1
        elif len(str(stones[0])) % 2 == 0:
            chars = str(stones[0])
            middle = len(chars) // 2
            stones[0] = int(chars[:middle])
            stones.rotate(-1)
            stones.insert(0, int(chars[middle:]))
        else:
            stones[0] = stones[0] * 2024

        stones.rotate(-1)


def part_1(puzzle: str) -> int:
    stones = parse_input(puzzle)

    for _ in range(0, 25):
        blink(stones)

    return len(stones)


def part_2(puzzle: str) -> int:
    stones = parse_input(puzzle)

    for _ in range(0, 75):
        blink(stones)

    return len(stones)


# -- Tests


def test_blink() -> None:
    stones = parse_input("0 1 10 99 999")

    blink(stones)
    assert stones == deque([1, 2024, 1, 0, 9, 9, 2021976])


def get_example_input() -> str:
    return "125 17"


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 55312


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 203457


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
