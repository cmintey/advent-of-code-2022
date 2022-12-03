from functools import reduce
import os
from pathlib import Path

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[str]:
    filepath = os.path.join(input_dir, filename)
    return Path(filepath).read_text().split("\n")


priorities = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def part_1(input: list[str]) -> int:
    score = 0
    for rucksack in input:
        mid = len(rucksack) // 2
        c1, c2 = set(rucksack[:mid]), set(rucksack[mid:])
        common = (c1 & c2).pop()
        score += priorities.index(common) + 1
    return score


def part_2(input: list[str]) -> int:
    score = 0
    group_size = 3
    for i in range(0, len(input), group_size):
        group = input[i : i + group_size]
        rucks = list(map(set, group))
        common = reduce(lambda x, y: x & y, rucks).pop()
        score += priorities.index(common) + 1
    return score


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
