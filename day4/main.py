import os
from pathlib import Path

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[str]:
    filepath = os.path.join(input_dir, filename)
    return Path(filepath).read_text().strip().split("\n")


def part_1(input: list[str]) -> int:
    c = 0
    for pair in input:
        r1, r2 = list(map(lambda x: x.split("-"), pair.split(",")))
        s1, s2 = set(range(int(r1[0]), int(r1[1]) + 1)), set(
            range(int(r2[0]), int(r2[1]) + 1)
        )
        inter = s1 & s2
        if s1 == inter or s2 == inter:
            c += 1
    return c


def part_2(input: list[str]) -> int:
    c = 0
    for pair in input:
        r1, r2 = list(map(lambda x: x.split("-"), pair.split(",")))
        s1, s2 = set(range(int(r1[0]), int(r1[1]) + 1)), set(
            range(int(r2[0]), int(r2[1]) + 1)
        )
        inter = s1 & s2
        if inter:
            c += 1
    return c


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
