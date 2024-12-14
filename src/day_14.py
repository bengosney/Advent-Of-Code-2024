import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from itertools import count
from math import prod

from utils import ImposibleError, no_input_skip, read_input


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    def move(self, extents: "Extent"):
        self.x = (self.x + self.vx) % extents.x
        self.y = (self.y + self.vy) % extents.y

    def complex(self) -> complex:
        return complex(self.x, self.y)


@dataclass(frozen=True)
class Extent:
    x: int
    y: int

    @cached_property
    def half_x(self) -> int:
        return self.x // 2

    @cached_property
    def half_y(self) -> int:
        return self.y // 2

    def quadrant(self, robot: Robot) -> int:
        if robot.x == self.half_x or robot.y == self.half_y:
            return 0

        return (1 if robot.x < self.half_x else 2) + (4 if robot.y > self.half_y else 8)


def parse_input(puzzle: str) -> list[Robot]:
    regex = re.compile(r"(-?\d+),(-?\d+)")

    robots = []
    for line in puzzle.splitlines():
        parts = regex.findall(line)
        px, py = int(parts[0][0]), int(parts[0][1])
        vx, vy = (int(parts[1][0]), int(parts[1][1]))
        robots.append(Robot(px, py, vx, vy))

    return robots


def part_1(puzzle: str, extents: Extent = Extent(101, 103)) -> int:
    robots = parse_input(puzzle)

    for _ in range(100):
        for robot in robots:
            robot.move(extents)

    quadrants = defaultdict(int)
    for robot in robots:
        quadrants[extents.quadrant(robot)] += 1
    del quadrants[0]

    return prod(quadrants.values())


def part_2(puzzle: str, extents: Extent = Extent(101, 103)) -> int:
    robots = parse_input(puzzle)
    robot_count = len(robots)

    for i in count():
        positions = set()
        for robot in robots:
            robot.move(extents)
            positions.add(robot.complex())

        if len(positions) == robot_count:
            return i + 1

    raise ImposibleError()


# -- Tests


def get_example_input() -> str:
    return """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input, Extent(11, 7)) == 12


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 208437768


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 7492


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
