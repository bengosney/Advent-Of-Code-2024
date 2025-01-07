import re
from dataclasses import dataclass

from utils import no_input_skip, read_input


@dataclass(frozen=True)
class Game:
    a: complex
    b: complex
    prize: complex

    def cost(self, error: int = 0) -> int:
        prize = self.prize + complex(error, error)

        numerator = prize.real * self.b.imag + prize.imag * -self.b.real
        denominator = self.a.real * self.b.imag + self.a.imag * -self.b.real
        a = numerator // denominator

        numerator = prize.real - self.a.real * a
        denominator = self.b.real
        b = numerator // denominator

        a_miss = self.a.real * a + self.b.real * b != prize.real
        b_miss = self.a.imag * a + self.b.imag * b != prize.imag

        return 0 if a_miss or b_miss else int(3 * a + b)


def parse_line(line: str) -> complex:
    number = re.compile(r"[\+\-]?\d+")
    x, y = line.split(" ")[-2:]

    return complex(int(number.findall(x)[0]), int(number.findall(y)[0]))


def parse_input(puzzle: str) -> list[Game]:
    games = []
    for parts in puzzle.split("\n\n"):
        lines = map(parse_line, parts.splitlines())
        games.append(Game(*lines))

    return games


def part_1(puzzle: str) -> int:
    games = parse_input(puzzle)

    return sum(game.cost() for game in games)


def part_2(puzzle: str) -> int:
    games = parse_input(puzzle)

    return sum(game.cost(10_000_000_000_000) for game in games)


# -- Tests


def get_example_input() -> str:
    return """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 480


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 875318608908


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 26299


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 107824497933339


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
