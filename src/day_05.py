from collections.abc import Iterable

from utils import no_input_skip, read_input


def process_input(puzzle: str) -> tuple[Iterable[tuple[int, int]], Iterable[list[int]]]:
    ordering, pages = puzzle.strip().split("\n\n")

    ordering_rules: Iterable[tuple[int, int]] = []
    for pair in ordering.split("\n"):
        rules = pair.split("|")
        ordering_rules.append((int(rules[0]), int(rules[1])))

    pages = [[int(page) for page in row.split(",")] for row in pages.strip().split("\n")]

    return ordering_rules, pages


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


def reorder(ordering: Iterable[tuple[int, int]], pages: list[int]) -> list[int]:
    attempts = 0
    while not in_order(ordering, pages) and attempts < 20:
        attempts += 1
        for pos, page in enumerate(pages):
            for pair in ordering:
                try:
                    if page == pair[1] and (idx := pages.index(pair[0])) > pos:
                        pages[pos], pages[idx] = pages[idx], pages[pos]  # noqa: PLR1736
                except ValueError:
                    pass

    return pages


def part_2(puzzle: str) -> int:
    ordering, all_pages = process_input(puzzle)

    total = 0
    for pages in all_pages:
        if not in_order(ordering, pages):
            ordered = reorder(ordering, pages)
            total += ordered[len(pages) // 2]

    return total


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


def test_part_2() -> None:
    test_input = get_example_input()
    assert part_2(test_input) == 123


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 5208


@no_input_skip
def test_part_2_real() -> None:
    real_input = read_input(__file__)
    assert part_2(real_input) == 6732


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
