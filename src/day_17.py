from collections import defaultdict

from utils import no_input_skip, read_input  # noqa: F401


def parse_input(puzzle: str) -> tuple[dict[str, int], list[int]]:
    raw_registers, raw_program = puzzle.split("\n\n")
    registers = defaultdict(int)
    program = []

    for line in raw_registers.split("\n"):
        register, value = line.split(": ")
        registers[register.split(" ")[1]] = int(value)

    program = [int(line) for line in raw_program.split(" ")[1].split(",")]

    return registers, program


def run_program(registers: dict[str, int], program: list[int]) -> list[int]:  # noqa: C901
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

    output = []

    ptr = 0
    while ptr < len(program):
        match program[ptr]:
            case 0:  # adv
                registers["A"] = registers["A"] // (2 ** op(program[ptr + 1]))
            case 1:  # bxl
                registers["B"] ^= program[ptr + 1]
            case 2:  # bst
                registers["B"] = op(program[ptr + 1]) % 8
            case 3:  # jnz
                if registers["A"] != 0:
                    ptr = program[ptr + 1]
                    continue
            case 4:  # bxc
                registers["B"] ^= registers["C"]
            case 5:  # out
                output.append(op(program[ptr + 1]) % 8)
            case 6:  # bdv
                registers["B"] = registers["A"] // (2 ** op(program[ptr + 1]))
            case 7:  # cdv
                registers["C"] = registers["A"] // (2 ** op(program[ptr + 1]))
            case _:
                raise NotImplementedError(program[ptr])
        ptr += 2

    return output


def part_1(puzzle: str) -> str:
    registers, program = parse_input(puzzle)

    output = run_program(registers, program)

    return ",".join(map(str, output))


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def test_run_program_1() -> None:
    registers = {"A": 0, "B": 0, "C": 9}
    program = [2, 6]

    run_program(registers, program)

    assert registers["B"] == 1


def test_run_program_2() -> None:
    registers = {"A": 10, "B": 0, "C": 0}
    program = [5, 0, 5, 1, 5, 4]

    assert run_program(registers, program) == [0, 1, 2]


def test_run_program_3() -> None:
    registers = {"A": 2024, "B": 0, "C": 0}
    program = [0, 1, 5, 4, 3, 0]

    assert run_program(registers, program) == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert registers["A"] == 0


def test_run_program_4() -> None:
    registers = {"A": 0, "B": 29, "C": 0}
    program = [1, 7]

    run_program(registers, program)
    assert registers["B"] == 26


def test_run_program_5() -> None:
    registers = {"A": 0, "B": 2024, "C": 43690}
    program = [4, 0]

    run_program(registers, program)
    assert registers["B"] == 44354


def get_example_input() -> str:
    return """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == "4,6,3,5,6,3,5,2,1,0"


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
