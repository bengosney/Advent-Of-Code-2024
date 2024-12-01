from collections import Counter

# First Party
from utils import no_input_skip, read_input


def process_list(puzzle: str) -> tuple[list[int], list[int]]:
    left = []
    right = []
    for line in puzzle.splitlines():
        parts = line.split(" ")
        left.append(int(parts[0]))
        right.append(int(parts[-1]))

    left.sort()
    right.sort()
    return left, right


def part_1(puzzle: str) -> int:
    left, right = process_list(puzzle)
    total: int = 0
    for i in range(len(left)):
        total += max(left[i], right[i]) - min(left[i], right[i])

    return total


def part_2(puzzle: str) -> int:
    left, right = process_list(puzzle)

    right_counts = Counter(right)
    total: int = 0
    for c in left:
        total += c * right_counts[c]

    return total


# -- Tests


def get_example_input() -> str:
    return """3   4
4   3
2   5
1   3
3   9
3   3"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 11


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 31


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 1651298


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 21306195


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
