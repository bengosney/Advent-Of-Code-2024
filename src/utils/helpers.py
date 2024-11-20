# Standard Library
import os
from collections.abc import Iterable


def read_input(day: str) -> str:
    file = os.path.splitext(os.path.basename(day))[0]
    with open(os.path.join(os.path.dirname(__file__), "..", "..", "inputs", f"{file}.txt")) as f:
        return f.read().rstrip().rstrip("\n\r")


def input_to_ints(input: str) -> list[int]:
    return [int(x) for x in input.splitlines()]


def ints_to_input(ints: Iterable[int]) -> str:
    return "\n".join([str(x) for x in ints])


ALPHABET = {
    ".##.\n#..#\n#..#\n####\n#..#\n#..#": "A",
    "###.\n#..#\n###.\n#..#\n#..#\n###.": "B",
    ".##.\n#..#\n#...\n#...\n#..#\n.##.": "C",
    "####\n#...\n###.\n#...\n#...\n####": "E",
    "####\n#...\n###.\n#...\n#...\n#...": "F",
    ".##.\n#..#\n#...\n#.##\n#..#\n.###": "G",
    "#..#\n#..#\n####\n#..#\n#..#\n#..#": "H",
    ".###\n..#.\n..#.\n..#.\n..#.\n.###": "I",
    "..##\n...#\n...#\n...#\n#..#\n.##.": "J",
    "#..#\n#.#.\n##..\n#.#.\n#.#.\n#..#": "K",
    "#...\n#...\n#...\n#...\n#...\n####": "L",
    ".##.\n#..#\n#..#\n#..#\n#..#\n.##.": "O",
    "###.\n#..#\n#..#\n###.\n#...\n#...": "P",
    "###.\n#..#\n#..#\n###.\n#.#.\n#..#": "R",
    ".###\n#...\n#...\n.##.\n...#\n###.": "S",
    "#..#\n#..#\n#..#\n#..#\n#..#\n.##.": "U",
    "#...\n#...\n.#.#\n..#.\n..#.\n..#.": "Y",
    "####\n...#\n..#.\n.#..\n#...\n####": "Z",
    "....\n....\n....\n....\n....\n....": "",
    "####\n#...\n#...\n#...\n####\n....": "TEST",
}


def ocr(input: dict[tuple[int, int], str]) -> str:
    all_x, _ = zip(*input)
    chars: str = ""
    char_count = max(all_x) // 4
    for i in range(char_count + 1):
        char: str = ""
        for y in range(6):
            for x in range(4):
                char += input[(x + (i * 5), y)]
            char += "\n"
        chars += ALPHABET[char.strip()]

    return "".join(chars).strip()


# --- tests


def test_read_input():
    assert read_input("day_00.py") == "123\n456\n012"


def test_input_to_ints():
    test_input = read_input("day_00.py")
    assert input_to_ints(test_input) == [123, 456, 12]


def test_ints_to_input():
    ints = [123, 456, 12]
    assert ints_to_input(ints) == "123\n456\n12"


def test_ocr_letters():
    for chars, letter in ALPHABET.items():
        grid: dict[tuple[int, int], str] = {}
        for y, line in enumerate(chars.split("\n")):
            for x, cell in enumerate(line):
                grid[(x, y)] = cell
        assert ocr(grid) == letter
