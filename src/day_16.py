from heapq import heappop, heappush

from utils import no_input_skip, read_input

Point = tuple[int, int]


def parse_input(puzzle: str) -> tuple[set[Point], Point, Point]:
    walls = set()

    for y, line in enumerate(puzzle.split("\n")):
        for x, cell in enumerate(line):
            if cell == "#":
                walls.add((x, y))
            elif cell == "S":
                start = (x, y)
            elif cell == "E":
                end = (x, y)
    return walls, start, end


def part_1(puzzle: str) -> int:
    walls, start, end = parse_input(puzzle)

    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    queue: list[tuple[int, int, int, int, int, set[tuple[int, int]]]] = []
    heappush(queue, (0, start[0], start[1], 1, 0, set()))
    scores: list = []

    seen = set()

    itterations = 0
    while queue:
        itterations += 1
        score, x, y, dx, dy, history = heappop(queue)
        print(f"{score=}, {x=}, {y=}, {dx=}, {dy=}")
        current_direction = (dx, dy)
        pos = (x, y)
        if pos in walls or pos in seen:
            continue

        seen.add(pos)

        if pos == end:
            scores.append(score)
            continue

        for direction in directions:
            next_pos = (x + direction[0], y + direction[1])
            if next_pos in history or next_pos in walls:
                continue

            next_score = score + 1
            if direction != current_direction:
                next_score += 1000

            heappush(queue, (next_score, next_pos[0], next_pos[1], direction[0], direction[1], history | {pos}))

    return min(scores)


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 7036


def test_part_1_2() -> None:
    test_input = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
    assert part_1(test_input) == 11048


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 115500


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
