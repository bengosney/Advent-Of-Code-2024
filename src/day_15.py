from dataclasses import dataclass, field

from utils import no_input_skip, read_input

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

    double_wide: bool = False
    box_links: dict[Box, Box] = field(default_factory=dict)

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
        move_box = self.move_box if not self.double_wide else self.move_box_double_wide
        if new_robot in self.walls:
            return False
        if new_robot in self.boxes:
            if not move_box(move, new_robot):
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

    def move_box_double_wide(self, move: Move, box: Box, checked: set[Box] = set()):
        new_box = box + move

        if box in checked:
            return True

        if new_box in self.walls:
            return False

        if new_box in self.boxes:
            if not self.move_box_double_wide(move, new_box, checked | {box}):
                return False

        if move not in [move_map["<"], move_map[">"]]:
            other_box = self.box_links[box]
            if not self.move_box_double_wide(move, other_box, checked | {box}):
                return False

        self.boxes.remove(box)
        self.boxes.append(new_box)

        self.box_links[new_box] = self.box_links[box]
        self.box_links[self.box_links[box]] = new_box
        del self.box_links[box]

        return True

    def score(self) -> int:
        score = 0

        def sort_complex(comp: complex):
            return comp.real + (comp.imag * 1000)

        scored = set()

        for box in sorted(self.boxes, key=sort_complex):
            if box not in scored:
                scored.add(box)
                try:
                    scored.add(self.box_links[box])
                except KeyError:
                    pass
                score += 100 * int(box.imag) + int(box.real)
        return score


def parse_input(puzzle: str, double_wide: bool = False) -> tuple[Warehouse, list[Move]]:
    warehouse, moves = puzzle.split("\n\n")
    robot = complex(0, 0)
    boxes = []
    walls = []
    box_links = {}
    mul = 2 if double_wide else 1
    for y, line in enumerate(warehouse.splitlines()):
        for x, cell in enumerate(line):
            pos = complex(x * mul, y)
            if cell == "@":
                robot = pos
            elif cell == "O":
                boxes.append(pos)
                if double_wide:
                    boxes.append(pos + 1)
                    box_links[pos + 1] = pos
                    box_links[pos] = pos + 1
            elif cell == "#":
                walls.append(pos)
                if double_wide:
                    walls.append(pos + 1)

    moves = [move_map[move] for move in moves.strip() if move in move_map]
    return Warehouse(robot, boxes, walls, double_wide, box_links), moves


def part_1(puzzle: str) -> int:
    warehouse, moves = parse_input(puzzle)

    for move in moves:
        warehouse.move(move)

    return warehouse.score()


def part_2(puzzle: str) -> int:
    warehouse, moves = parse_input(puzzle, double_wide=True)

    warehouse.draw()
    for move in moves:
        warehouse.move(move)
    warehouse.draw()

    return warehouse.score()


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


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 9021


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 1577255


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 1597035


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
