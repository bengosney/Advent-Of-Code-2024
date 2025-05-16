import re

from utils import no_input_skip, read_input


def part_1(puzzle: str) -> int:
    return sum(int(a) * int(b) for a, b in re.findall(r"mul\((\d+),(\d+)\)", puzzle))


def part_2(puzzle: str) -> int:
    working = True
    total = 0
    for match in re.finditer(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", puzzle):
        match [x for x in match.groups() if x is not None]:
            case ["do()"]:
                working = True
            case ["don't()"]:
                working = False
            case [a, b]:
                total += (int(a) * int(b)) * working

    return total


# -- Tests


def get_example_input_part_1() -> str:
    return "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"


def get_example_input_part_2() -> str:
    return "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def test_part_1() -> None:
    test_input = get_example_input_part_1()
    assert part_1(test_input) == 161


def test_part_2() -> None:
    test_input = get_example_input_part_2()
    assert part_2(test_input) == 48


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 188116424


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 104245808


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
