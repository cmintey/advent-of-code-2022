import os
from pathlib import Path

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[str]:
    filepath = os.path.join(input_dir, filename)
    return Path(filepath).read_text().strip().split("\n")


def part_1(input: list[str]) -> int:
    c = 0
    for pair in input:
        ranges = map(lambda x: x.split("-"), pair.split(","))
        s1, s2 = [set(range(int(x[0]), int(x[1]) + 1)) for x in ranges]
        if s1.issubset(s2) or s2.issubset(s1):
            c += 1
    return c


def part_2(input: list[str]) -> int:
    c = 0
    for pair in input:
        ranges = map(lambda x: x.split("-"), pair.split(","))
        s1, s2 = [set(range(int(x[0]), int(x[1]) + 1)) for x in ranges]
        inter = s1 & s2
        if inter:
            c += 1
    return c


def part_1_compare(input: list[str]) -> int:
    y = 0
    for pair in input:
        ranges = map(lambda x: x.split("-"), pair.split(","))
        (a, b), (c, d) = [(int(x[0]), int(x[1])) for x in ranges]
        """
              a ----- b
            c ---------- d
        ---------------------
            a --------- b
               c --- d
        """
        if a <= c and b >= d or c <= a and d >= b:
            y += 1
    return y


def part_2_compare(input: list[str]) -> int:
    y = 0
    for pair in input:
        ranges = map(lambda x: x.split("-"), pair.split(","))
        (a, b), (c, d) = [(int(x[0]), int(x[1])) for x in ranges]
        """
              a ----- b
            c --- d
        ---------------------
            a - b
               c --- d
        """
        if a <= c <= b or c <= a <= d or a <= d <= b or c <= b <= d:
            y += 1
    return y


input = parse_input("input.txt")

# initial solution using sets
print(part_1(input))
print(part_2(input))

# second solution doing direct comparison
print(part_1_compare(input))
print(part_2_compare(input))
