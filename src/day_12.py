from collections import defaultdict, deque

from icecream import ic

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
    m: dict[complex, str] = defaultdict(str)

    def p(*args, **kwargs):
        if debug:
            ic(*args, **kwargs)

    perimeter = 0
    for pos in patch:
        m[pos] = "X"
        p(f"{pos=}")
        for neighbor in get_neighbors(pos):
            p(f"{neighbor=}")
            if neighbor not in patch:
                perimeter += 1
                m[neighbor] = "~"

    if debug:
        size = 10
        for y in range(size):
            for x in range(size):
                print(m.get(complex(x, y), " "), end="")
            print()

    return perimeter


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

        # perimeter = get_perimeter(patch)
        # print(f"{plant=} {len(patch)=} {perimeter=} = {len(patch) * perimeter}")
        cost += len(patch) * get_perimeter(patch)

    return cost


def part_2(puzzle: str) -> int:
    pass


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


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 1473276


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
