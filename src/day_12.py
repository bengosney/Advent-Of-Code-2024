from collections import defaultdict, deque

from utils import no_input_skip, read_input


def parse_input(puzzle: str) -> dict[complex, str]:
    garden = defaultdict(str)

    for y, line in enumerate(puzzle.split("\n")):
        for x, cell in enumerate(line):
            garden[complex(x, y)] = cell

    return garden


def get_directions() -> list[complex]:
    return [(1 + 0j), (-1 + 0j), (0 + 1j), (0 - 1j)]


def get_neighbors(pos: complex) -> list[complex]:
    return [pos + dir for dir in get_directions()]


def get_perimeter(patch: set[complex], debug=False) -> int:
    perimeter = 0
    for pos in patch:
        for neighbor in get_neighbors(pos):
            if neighbor not in patch:
                perimeter += 1

    return perimeter


def get_edges(patch: set[complex], debug=False) -> int:
    left = complex(-1, 0)
    right = complex(1, 0)
    up = complex(0, -1)
    down = complex(0, 1)
    checked_left = set()
    checked_right = set()
    checked_up = set()
    checked_down = set()

    def walk_dir(start: complex, direction: complex, other: complex, checked: set) -> None:
        current = start
        while True:
            if (current + other) not in patch or current in patch:
                break

            checked.add(current)
            current += direction

    edges = 0
    for pos in patch:
        if (e := pos + left) not in patch and e not in checked_left:
            edges += 1
            walk_dir(e, down, right, checked_left)
            walk_dir(e, up, right, checked_left)
        if (e := pos + right) not in patch and e not in checked_right:
            edges += 1
            walk_dir(e, down, left, checked_right)
            walk_dir(e, up, left, checked_right)

        if (e := pos + up) not in patch and e not in checked_up:
            edges += 1
            walk_dir(e, left, down, checked_up)
            walk_dir(e, right, down, checked_up)
        if (e := pos + down) not in patch and e not in checked_down:
            edges += 1
            walk_dir(e, left, up, checked_down)
            walk_dir(e, right, up, checked_down)

    return edges


def part_1(puzzle: str) -> int:
    garden = parse_input(puzzle)
    visited = set()

    cost = 0

    for pos, cell in garden.items():
        if pos in visited:
            continue

        plant = cell
        patch = set([pos])
        to_check = deque([pos])
        while to_check:
            current = to_check.popleft()
            visited.add(current)

            for neighbor in get_neighbors(current):
                if garden.get(neighbor) == plant and neighbor not in visited:
                    to_check.append(neighbor)
                    patch.add(neighbor)
                    visited.add(neighbor)

        cost += len(patch) * get_perimeter(patch)

    return cost


def part_2(puzzle: str) -> int:
    garden = parse_input(puzzle)
    visited = set()

    cost = 0

    for pos, cell in garden.items():
        if pos in visited:
            continue

        plant = cell
        patch = set([pos])
        to_check = deque([pos])
        while to_check:
            current = to_check.popleft()
            visited.add(current)

            for neighbor in get_neighbors(current):
                if garden.get(neighbor) == plant and neighbor not in visited:
                    to_check.append(neighbor)
                    patch.add(neighbor)
                    visited.add(neighbor)

        cost += len(patch) * get_edges(patch)

    return cost


# -- Tests


def get_example_input() -> str:
    return """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 1930


def test_part_2_1() -> None:
    test_input = """AAAA
BBCD
BBCC
EEEC"""
    assert part_2(test_input) == 80


def test_part_2_2() -> None:
    test_input = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
    assert part_2(test_input) == 436


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 1206


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 1473276


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 901100


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
