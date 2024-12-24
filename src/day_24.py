from typing import Literal, cast

import pytest

from utils import ImposibleError, no_input_skip, read_input

Wire = str
Op = Literal["AND", "OR", "XOR"]
Rule = tuple[Wire, Op, Wire, Wire]


def parse_input(puzzle: str) -> tuple[dict[Wire, bool], dict[Wire, Rule]]:
    parts = puzzle.split("\n\n")

    def parse_wire(wire: str) -> Wire:
        return wire

    def parse_op(op: str) -> Op:
        if op in ["AND", "OR", "XOR"]:
            return cast(Op, op)
        else:
            raise ValueError(op)

    wires: dict[Wire, bool] = {}
    for line in parts[0].splitlines():
        wire, value = line.split(": ")
        wires[parse_wire(wire)] = int(value) == 1

    rules: dict[Wire, Rule] = {}
    for line in parts[1].splitlines():
        parts = line.split(" ")
        rule: Rule = (parse_wire(parts[0]), parse_op(parts[1]), parse_wire(parts[2]), parse_wire(parts[4]))
        rules[rule[3]] = rule

    return wires, rules


def apply_rule(rule: Rule, wires: dict[Wire, bool], rules: dict[Wire, Rule]) -> None:
    a, op, b, c = rule

    if a not in wires:
        apply_rule(rules[a], wires, rules)
    if b not in wires:
        apply_rule(rules[b], wires, rules)

    match op:
        case "AND":
            wires[c] = wires[a] and wires[b]
        case "OR":
            wires[c] = wires[a] or wires[b]
        case "XOR":
            wires[c] = wires[a] != wires[b]
        case _:
            raise ImposibleError(op)


def part_1(puzzle: str) -> int:
    wires, rules = parse_input(puzzle)

    for rule in rules.values():
        apply_rule(rule, wires, rules)

    result_wires = sorted([w for w in wires.keys() if w.startswith("z")])
    result = [str(int(wires[wire])) for wire in result_wires]
    result.reverse()

    return int("".join(map(lambda x: str(int(x)), result)), 2)


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_small_example_input() -> str:
    return """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""


def get_big_example_input() -> str:
    return """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (get_small_example_input(), 4),
        (get_big_example_input(), 2024),
    ],
)
def test_part_1(test_input, expected) -> None:
    assert part_1(test_input) == expected


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 51715173446832


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
