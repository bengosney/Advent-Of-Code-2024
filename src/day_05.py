from collections.abc import Iterable

from utils import no_input_skip, read_input


def process_input(puzzle: str) -> tuple[Iterable[Iterable[int]], Iterable[list[int]]]:
    ordering, pages = puzzle.strip().split("\n\n")
    ordering = [tuple(map(int, pair.split("|"))) for pair in ordering.split("\n")]

    pages = [[int(page) for page in row.split(",")] for row in pages.strip().split("\n")]

    return ordering, pages


def in_order(ordering: Iterable[tuple[int, int]], pages: list[int]) -> bool:
    for pos, page in enumerate(pages):
        for pair in ordering:
            if page == pair[1] and pair[0] in pages[pos + 1 :]:
                return False
    return True


def part_1(puzzle: str) -> int:
    ordering, all_pages = process_input(puzzle)

    total = 0
    for pages in all_pages:
        if in_order(ordering, pages):
            total += pages[len(pages) // 2]

    return total


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 143


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) == 123


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 5208


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
