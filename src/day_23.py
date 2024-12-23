from collections import defaultdict
from itertools import combinations

from utils import no_input_skip, read_input


def map_input(puzzle: str) -> dict[str, set[str]]:
    graph = defaultdict(set)
    pairs = [line.split("-") for line in puzzle.split("\n")]
    for a, b in pairs:
        graph[a].add(b)
        graph[b].add(a)

    return graph


def part_1(puzzle: str) -> int:
    graph = map_input(puzzle)
    checked: set[str] = set()

    posible_found = 0
    groups_of_three: set[frozenset[str]] = set()

    for looking_at, nodes in graph.items():
        if any(node in checked for node in nodes):
            continue

        for a, b in combinations(nodes, 2):
            if a in graph[b]:
                groups_of_three.add(frozenset([looking_at, a, b]))

    for group in groups_of_three:
        if any(node[0] == "t" for node in group):
            posible_found += 1

    return posible_found


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 7


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 1330


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
