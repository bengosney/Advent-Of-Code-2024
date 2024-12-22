from utils import no_input_skip, read_input


def mix(n1: int, n2: int) -> int:
    return n1 ^ n2


def prune(n: int) -> int:
    return n % 16777216


def mix_prune(n1: int, n2: int) -> int:
    return prune(mix(n1, n2))


def secret_number(seed: int) -> int:
    number = seed

    number = mix_prune(number * 64, number)
    number = mix_prune(number // 32, number)
    number = mix_prune(number * 2048, number)

    return number


def part_1(puzzle: str) -> int:
    numbers = []

    for line in map(int, puzzle.splitlines()):
        number = line
        for _ in range(2000):
            number = secret_number(number)
        numbers.append(number)

    return sum(numbers)


def part_2(puzzle: str) -> int:
    pass


# -- Tests


def test_secret_number() -> None:
    results = [15887950, 16495136, 527345, 704524, 1553684, 12683156, 11100544, 12249484, 7753432, 5908254]
    seed = 123

    for result in results:
        assert secret_number(seed) == result
        seed = result


def test_mix() -> None:
    assert mix(42, 15) == 37


def test_prune() -> None:
    assert prune(100000000) == 16113920


def get_example_input() -> str:
    return """1
10
100
2024"""


def test_part_1() -> None:
    test_input = get_example_input()
    assert part_1(test_input) == 37327623


# def test_part_2() -> None:
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real() -> None:
    real_input = read_input(__file__)
    assert part_1(real_input) == 19241711734


# @no_input_skip
# def test_part_2_real() -> None:
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")
