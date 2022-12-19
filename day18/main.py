import os
import math
from collections import deque

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[list[int]]:
    filepath = os.path.join(input_dir, filename)
    return list(
        map(
            lambda s: tuple(map(int, s.split(","))),
            open(filepath).read().strip().split("\n"),
        )
    )


def distance(a, b):
    return math.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2) + pow(a[2] - b[2], 2))


def neighbors(x, y, z):
    return set(
        [
            (x - 1, y, z),
            (x + 1, y, z),
            (x, y - 1, z),
            (x, y + 1, z),
            (x, y, z - 1),
            (x, y, z + 1),
        ]
    )


def part_1(cubes: list[list[int]]) -> int:
    sa = 6 * len(cubes)
    all_cubes = set(cubes)
    for cube in all_cubes:
        if touching := (neighbors(*cube) & all_cubes):
            sa -= len(touching)

    return sa


def part_2(cubes: list[list[int]]) -> int:
    all_cubes = set(cubes)
    min_x, max_x = min(all_cubes)[0], max(all_cubes)[0]
    min_y, max_y = (
        min(all_cubes, key=lambda b: b[1])[1],
        max(all_cubes, key=lambda b: b[1])[1],
    )
    min_z, max_z = (
        min(all_cubes, key=lambda b: b[2])[2],
        max(all_cubes, key=lambda b: b[2])[2],
    )

    air = set([(min_x - 1, min_y - 1, min_z - 1)])
    q = deque([(min_x - 1, min_y - 1, min_z - 1)])
    while q:
        w = q.popleft()

        if (
            min_x - 1 <= w[0] <= max_x + 1
            and min_y - 1 <= w[1] <= max_y + 1
            and min_z - 1 <= w[2] <= max_z + 1
        ):

            w_neigh = neighbors(*w) - air - all_cubes
            air.update(w_neigh)
            q.extend(list(w_neigh))

    return sum((s in air) for c in all_cubes for s in neighbors(*c))


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
