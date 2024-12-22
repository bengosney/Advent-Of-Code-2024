from collections import defaultdict, deque

import pytest

from utils import no_input_skip, read_input


def secret_number(seed: int) -> int:
    number = seed

    number = (number ^ (number * 64)) % 16777216
    number = (number ^ (number // 32)) % 16777216
    number = (number ^ (number * 2048)) % 16777216

    return number


def part_1(puzzle: str) -> int:
    numbers = []

    for start in map(int, puzzle.splitlines()):
        number = start
        for _ in range(2000):
            number = secret_number(number)
        numbers.append(number)

    return sum(numbers)


def part_2(puzzle: str) -> int:
    bananas = defaultdict(int)

    for start in map(int, puzzle.splitlines()):
        sequences = {}
        changes = deque(maxlen=4)
        number = start
        previous = start % 10
        for _ in range(2000):
            number = secret_number(number)
            number_cost = number % 10
            changes.append(number_cost - previous)
            if len(changes) == 4 and tuple(changes) not in sequences:
                sequences[tuple(changes)] = number_cost
            previous = number_cost

        for sequence, banana in sequences.items():
            bananas[sequence] += banana

    return max(bananas.values())


# -- Tests


def test_secret_number() -> None:
    results = [15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]
    seed = 123

    for result in results:
        assert secret_number(seed) == result
        seed = result


def get_example_input() -> str:
    return """1
10
100
2024"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 37327623


def test_part_2() -> None:
    test_input = """1
2
3
2024"""
    assert part_2(test_input) == 23


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 19241711734


@no_input_skip
@pytest.mark.slow()
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 2058


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
