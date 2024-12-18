from collections import defaultdict
from heapq import heappop, heappush

from utils import no_input_skip, read_input  # noqa: F401


def parse_input(puzzle: str) -> list[complex]:
    return [complex(int(x), int(y)) for x, y in (line.split(",") for line in puzzle.split("\n"))]


def part_1(puzzle: str, size: int = 70, sim_len: int = 1024) -> int:  # noqa: C901
    bytes = parse_input(puzzle)
    grid = defaultdict(lambda: ".")

    def draw_grid():
        for y in range(size + 2):
            for x in range(size + 2):
                print(grid[complex(x, y)], end="")
            print()

    for byte in bytes[:sim_len]:
        grid[byte] = "#"

    visited: set[complex] = set()
    queue: list[tuple[int, int, int, set[complex]]] = []

    best_score = 0
    best_history = set()
    heappush(queue, (0, 0, 0, set([complex(0, 0)])))
    while queue:
        dist, x, y, history = heappop(queue)
        pos = complex(x, y)

        if pos in visited or pos in bytes[:sim_len]:
            continue

        visited.add(pos)

        if x == size and y == size:
            best_score = dist
            best_history = history
            break

        for direction in [complex(0, -1), complex(1, 0), complex(0, 1), complex(-1, 0)]:
            next_pos = pos + direction

            if next_pos.imag < 0 or next_pos.imag > size or next_pos.real < 0 or next_pos.real > size:
                continue

            if next_pos not in visited:
                heappush(queue, (dist + 1, int(next_pos.real), int(next_pos.imag), history | {pos}))

    for pos in best_history:
        grid[pos] = "O"

    # draw_grid()

    return best_score


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input, 6, 12) == 22


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
