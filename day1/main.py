import os
import heapq
from pathlib import Path

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[int]:
    filepath = os.path.join(input_dir, filename)
    return list(
        map(
            lambda x: sum(map(int, x.strip().split("\n"))),
            Path(filepath).read_text().split("\n\n"),
        )
    )


def part_1(input: list[int]) -> int:
    return max(input)


def part_2(input: list[int]) -> int:
    return sum(heapq.nlargest(3, input))


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
