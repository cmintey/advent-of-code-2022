import os
import re
from pathlib import Path

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> tuple[str, str]:
    filepath = os.path.join(input_dir, filename)
    state, moves = Path(filepath).read_text().split("\n\n")
    return state, moves


def get_initial_state(state: str) -> list[list[str]]:
    """
                [D]
    state:  [N] [C]
            [Z] [M] [P]
             1   2   3

    output: [[N, Z], [D, C, M], [P]]
    """
    lines = state.split("\n")
    N = len(lines)
    n = int(re.findall("\d+", lines[-1])[-1])
    stacks = [[] for _ in range(n)]
    for i, line in enumerate(reversed(lines)):
        if i == 0:
            pass
        for j in range(0, len(line), 4):
            crate = re.findall("[A-Za-z]+", line[j : j + 4])
            if crate:
                stacks[j // 4].append(crate[0])
    return stacks


def parse_move(move: str) -> list[int]:
    """
    move: `move n from s1 to s2`

    out: [n, s1, s2]
    """
    return list(map(int, re.findall("\d+", move)))


def get_answer(stacks: list[list[str]]) -> str:
    return "".join([x.pop() for x in stacks])


def part_1(state: str, moves: str) -> str:
    """
    Move n from s1 to s2 by directly popping s1 onto s2
    """
    stacks = get_initial_state(state)
    for move in moves.split("\n"):
        n, s1, s2 = parse_move(move)
        for _ in range(n):
            stacks[s2 - 1].append(stacks[s1 - 1].pop())
    return get_answer(stacks)


def part_2(state: str, moves: str) -> str:
    """
    Move n from s1 to s2, but can move several at once.
    To mimick, pop s1 onto intermediate stack (s3), then
    pop s3 onto s2
    """
    stacks = get_initial_state(state)
    for move in moves.split("\n"):
        n, s1, s2 = parse_move(move)
        inter = []
        for _ in range(n):
            inter.append(stacks[s1 - 1].pop())
        while inter:
            stacks[s2 - 1].append(inter.pop())
    return get_answer(stacks)


input = parse_input("input.txt")

print(part_1(*input))
print(part_2(*input))
