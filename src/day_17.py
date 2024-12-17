from collections import defaultdict, deque

from utils import no_input_skip, read_input  # noqa: F401


def parse_input(puzzle: str) -> tuple[dict[str, int], deque[int]]:
    raw_registers, raw_program = puzzle.split("\n\n")
    registers = defaultdict(int)
    program = []

    for line in raw_registers.split("\n"):
        register, value = line.split(": ")
        registers[register.split(" ")[1]] = int(value)

    program = deque([int(line) for line in raw_program.split(" ")[1].split(",")])

    return registers, program


def part_1(puzzle: str) -> int:  # noqa: C901
    registers, program = parse_input(puzzle)

    program = deque([0, 1, 2, 3])

    def op(operand) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return registers["A"]
            case 5:
                return registers["B"]
            case 6:
                return registers["C"]
            case 7:
                raise NotImplementedError
            case _:
                raise ValueError(operand)

    for _ in range(len(program)):
        ins = program[0]
        program.rotate(-1)
        match ins:
            case 0:  # adv
                value = op(program[0])
                program.rotate(-1)
                registers["A"] = int(registers["A"] / (2**value))
            case 1:  # bxl
                value = op(program[0])
                program.rotate(-1)
                registers["B"] = registers["B"] | value
            case 2:  # bst
                value = op(program[0])
                registers["B"] = value % 8
            case 3:  # jnz
                pass
            case _:
                print("Unknown instruction")

    print(registers)


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 4635635210


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
