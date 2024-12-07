from collections.abc import Callable, Iterable
from dataclasses import dataclass
from operator import add, mul

import pytest

from utils import no_input_skip, read_input


@dataclass(frozen=True)
class Calibration:
    answer: int
    test_values: list[int]


def calculate(values: list[int], operators: list[Callable]) -> Iterable[int]:
    if len(values) == 1:
        return values

    answers = []
    for calculated in calculate(values[1:], operators):
        answers.extend([op(calculated, values[0]) for op in operators])

    return answers


def parse_input(puzzle: str) -> Iterable[Calibration]:
    for line in puzzle.splitlines():
        parts = line.split(":")
        answer = int(parts[0])
        test_values = list(map(int, parts[1].split()))
        yield Calibration(answer, test_values)


def part_1(puzzle: str) -> int:
    total = 0
    calibrations = parse_input(puzzle)
    for calibration in calibrations:
        values = calibration.test_values
        values.reverse()
        answers = calculate(values, [add, mul])
        if any(answer == calibration.answer for answer in answers):
            total += calibration.answer

    return total


def concatenation(a: int, b: int) -> int:
    return int(str(a) + str(b))


def part_2(puzzle: str) -> int:
    total = 0
    calibrations = parse_input(puzzle)
    for calibration in calibrations:
        values = calibration.test_values
        values.reverse()
        answers = calculate(values, [add, mul, concatenation])
        if any(answer == calibration.answer for answer in answers):
            total += calibration.answer

    return total


# -- Tests


def test_concatenation() -> None:
    assert concatenation(12, 345) == 12345


def get_example_input() -> str:
    return """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 3749


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 11387


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 5512534574980


@no_input_skip
@pytest.mark.slow
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 328790210468594


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
