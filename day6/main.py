import os
from pathlib import Path

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> str:
    filepath = os.path.join(input_dir, filename)
    return Path(filepath).read_text().strip()


def unique_window(txt: str, size: int) -> int:
    """
    Iterates through the `txt` with the given window `size` and
    creates a set of the window to check the length.
    O(kn) where k=len(txt) and n=size
    """
    for i in range(len(txt)):
        if len(set(txt[i : i + size])) == size:
            return i + size


def linear_window(txt: str, size: int) -> int:
    """
    Iteratest through the `txt` with the given window `size` and
    creates a dictionary of the items in the window with a count of
    how many there are in that window.
    O(n) where n=len(txt)
    """
    seen = {}
    i = 0
    while len(seen) < size:
        if txt[i] not in seen:
            seen[txt[i]] = 0
        seen[txt[i]] += 1

        if i >= size:
            seen[txt[i - size]] -= 1
            if seen[txt[i - size]] == 0:
                del seen[txt[i - size]]
        i += 1
    return i


def part_1(code: str) -> int:
    return linear_window(code, 4)


def part_2(code: str) -> int:
    return linear_window(code, 14)


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
