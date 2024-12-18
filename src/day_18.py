from heapq import heappop, heappush

from utils import no_input_skip, read_input


class NoSolutionError(Exception):
    pass


class NoPathError(Exception):
    pass


def parse_input(puzzle: str) -> list[complex]:
    return [complex(int(x), int(y)) for x, y in (line.split(",") for line in puzzle.split("\n"))]


def walk_path(bytes: list[complex], size: int) -> set[complex]:
    visited: set[complex] = set()
    queue: list[tuple[int, int, int, set[complex]]] = []

    heappush(queue, (0, 0, 0, set([complex(0, 0)])))
    while queue:
        dist, x, y, history = heappop(queue)
        pos = complex(x, y)

        if pos in visited or pos in bytes:
            continue

        visited.add(pos)

        if x == size and y == size:
            return history

        for direction in [complex(0, -1), complex(1, 0), complex(0, 1), complex(-1, 0)]:
            next_pos = pos + direction

            if next_pos.imag < 0 or next_pos.imag > size or next_pos.real < 0 or next_pos.real > size:
                continue

            if next_pos not in visited:
                heappush(queue, (dist + 1, int(next_pos.real), int(next_pos.imag), history | {pos}))

    raise NoPathError()


def part_1(puzzle: str, size: int = 70, sim_len: int = 1024) -> int:
    bytes = parse_input(puzzle)
    path = walk_path(bytes[:sim_len], size)

    return len(path)


def part_2(puzzle: str, size: int = 70, inital_sim_length: int = 1024) -> str:
    bytes = parse_input(puzzle)
    sim_length = inital_sim_length

    for _ in range(len(bytes) - inital_sim_length):
        try:
            path = walk_path(bytes[:sim_length], size)
            for i in range(sim_length, len(bytes)):
                if bytes[i] in path:
                    sim_length = i + 1
                    break
        except NoPathError:
            break
    else:
        raise NoSolutionError()

    return f"{int(bytes[sim_length-1].real)},{int(bytes[sim_length-1].imag)}"


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


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input, 6, 12) == "6,1"


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 348


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == "54,44"


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
