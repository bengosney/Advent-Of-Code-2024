from itertools import product

from utils import no_input_skip, read_input

Lock = list[int]
Key = list[int]


def parse_input(puzzle: str) -> tuple[list[Key], list[Lock]]:
    keys = []
    locks = []

    for data in puzzle.split("\n\n"):
        lines = data.splitlines()
        item = [sum(int(lines[j][i] == "#") for j in range(len(lines))) - 1 for i in range(len(lines[0]))]
        if data.startswith("#"):
            keys.append(item)
        else:
            locks.append(item)

    return keys, locks


def fits(lock, key):
    for i in range(len(lock)):
        if lock[i] + key[i] > 5:
            return False
    return True


def part_1(puzzle: str) -> int:
    keys, locks = parse_input(puzzle)

    count = 0

    for key, lock in product(keys, locks):
        if fits(lock, key):
            count += 1

    return count


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""


def test_parse_key_input() -> None:
    keys, locks = parse_input("""#####
.####
.####
.####
.#.#.
.#...
.....""")
    assert keys == [[0, 5, 3, 4, 3]]


def test_parse_lock_input() -> None:
    keys, locks = parse_input(""".....
#....
#....
#...#
#.#.#
#.###
#####""")
    assert locks == [[5, 0, 2, 1, 3]]


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 3


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 3508


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
