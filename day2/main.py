from functools import reduce
import os
import heapq
from pathlib import Path

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[list[str]]:
    filepath = os.path.join(input_dir, filename)
    return list(
        map(lambda x: x.strip().split(" "), Path(filepath).read_text().split("\n"))
    )


# A: Rock; B: Paper; C: Scissors
# A beats C
# B beats A
# C beat B
winning_hands = {"A": "C", "B": "A", "C": "B"}


def score_round(a: str, b: str) -> int:
    score = 1 if b == "A" else 2 if b == "B" else 3
    score += 3 if a == b else 6 if winning_hands[b] == a else 0
    return score


def part_1(input: list[list[str]]) -> int:
    return reduce(lambda x, y: x + score_round(y[0], chr(ord(y[1]) - 23)), input, 0)


def part_2(input: list[list[str]]) -> int:
    tot = 0
    for round in input:
        opp, out = round
        draw, loss = opp, winning_hands[opp]
        win = (set(["A", "B", "C"]) - set([draw, loss])).pop()
        me = draw if out == "Y" else win if out == "Z" else loss
        tot += score_round(opp, me)
    return tot


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
