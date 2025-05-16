from collections import defaultdict, deque
from functools import partial

from utils import NoSolutionError, no_input_skip, read_input


def parse_input(puzzle: str) -> tuple[dict[str, int], list[int]]:
    raw_registers, raw_program = puzzle.split("\n\n")
    registers = defaultdict(int)
    program = []

    for line in raw_registers.split("\n"):
        register, value = line.split(": ")
        registers[register.split(" ")[1]] = int(value)

    program = [int(line) for line in raw_program.split(" ")[1].split(",")]

    return registers, program


def op(operand, registers) -> int:
    register_map = {4: "A", 5: "B", 6: "C"}
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4 | 5 | 6:
            return registers[register_map[operand]]
        case _:
            raise ValueError(operand)


def run_program(registers: dict[str, int], program: list[int]) -> list[int]:  # noqa: C901
    output = []
    ptr = 0
    getop = partial(op, registers=registers)
    while ptr < len(program):
        opcode = program[ptr + 1]
        match program[ptr]:
            case 0:  # adv
                registers["A"] = registers["A"] // (2 ** getop(opcode))
            case 1:  # bxl
                registers["B"] ^= opcode
            case 2:  # bst
                registers["B"] = getop(opcode) % 8
            case 3:  # jnz
                if registers["A"] != 0:
                    ptr = opcode
                    continue
            case 4:  # bxc
                registers["B"] ^= registers["C"]
            case 5:  # out
                output.append(getop(opcode) % 8)
            case 6:  # bdv
                registers["B"] = registers["A"] // (2 ** getop(opcode))
            case 7:  # cdv
                registers["C"] = registers["A"] // (2 ** getop(opcode))
            case _:
                raise NotImplementedError(program[ptr])
        ptr += 2

    return output


def part_1(puzzle: str) -> str:
    registers, program = parse_input(puzzle)

    output = run_program(registers, program)

    return ",".join(map(str, output))


def part_2(puzzle: str) -> int:
    registers, program = parse_input(puzzle)

    queue = deque([(0, 1)])
    while queue:
        register_a, n = queue.popleft()
        if n > len(program):
            return register_a

        for i in range(8):
            next_a = (register_a * 8) + i
            result = run_program({**registers, "A": next_a}, program)

            if result == program[-n:]:
                queue.append((next_a, n + 1))

    raise NoSolutionError()


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


def test_part_1() -> None:
    test_input = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    assert part_1(test_input) == "4,6,3,5,6,3,5,2,1,0"


def test_part_2() -> None:
    test_input = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
    assert part_2(test_input) == 117440


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == "4,6,1,4,2,1,3,1,6"


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
