from dataclasses import dataclass

from utils import no_input_skip, read_input  # noqa: F401

Robot = complex
Box = complex
Wall = complex
Move = complex

move_map = {
    "<": complex(-1, 0),
    ">": complex(1, 0),
    "^": complex(0, -1),
    "v": complex(0, 1),
}


@dataclass
class Warehouse:
    robot: Robot
    boxes: list[Box]
    walls: list[Wall]

    def draw(self):
        min_x = min_y = 0
        max_x = max_y = 0
        for pos in self.walls:
            min_x = int(min(min_x, pos.real))
            min_y = int(min(min_y, pos.imag))
            max_x = int(max(max_x, pos.real))
            max_y = int(max(max_y, pos.imag))

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                pos = complex(x, y)
                if pos == self.robot:
                    print("@", end="")
                elif pos in self.boxes:
                    print("O", end="")
                elif pos in self.walls:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def move(self, move: Move):
        new_robot = self.robot + move
        if new_robot in self.walls:
            return False
        if new_robot in self.boxes:
            if not self.move_box(move, new_robot):
                return False

        self.robot = new_robot
        return True

    def move_box(self, move: Move, box: Box):
        new_box = box + move
        if new_box in self.walls:
            return False

        if new_box in self.boxes:
            if not self.move_box(move, new_box):
                return False

        self.boxes.remove(box)
        self.boxes.append(new_box)

        return True

    def score(self) -> int:
        score = 0
        for box in self.boxes:
            score += 100 * int(box.imag) + int(box.real)
        return score


def parse_input(puzzle: str) -> tuple[Warehouse, list[Move]]:
    warehouse, moves = puzzle.split("\n\n")
    robot = complex(0, 0)
    boxes = []
    walls = []
    for y, line in enumerate(warehouse.splitlines()):
        for x, cell in enumerate(line):
            pos = complex(x, y)
            if cell == "@":
                robot = pos
            elif cell == "O":
                boxes.append(pos)
            elif cell == "#":
                walls.append(pos)

    moves = [move_map[move] for move in moves.strip() if move in move_map]
    return Warehouse(robot, boxes, walls), moves


def part_1(puzzle: str) -> int:
    warehouse, moves = parse_input(puzzle)

    for move in moves:
        warehouse.move(move)

    return warehouse.score()


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) is not None


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


# @no_input_skip
# def test_part_1_real() -> None:
#     real_input = read_input(__file__)
#     assert part_1(real_input) is not None


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
