import os
import re
from tqdm import tqdm

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> dict[tuple[int, int], tuple[int, int]]:
    filepath = os.path.join(input_dir, filename)
    lines = open(filepath).read().strip().split("\n")
    sensor_map = {}
    for line in lines:
        sx, sy, bx, by = map(int, re.findall(r"-?\d+", line))
        sensor_map[sx, sy] = (bx, by)

    return sensor_map


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def part_1(sensor_map: dict[tuple[int, int], tuple[int, int]]) -> int:
    c = 0
    Y = 2000000
    sensor_coverage = {k: distance(k, v) for k, v in sensor_map.items()}

    min_x, max_x = (
        min(sensor_map.values(), key=lambda x: x[0])[0] - max(sensor_coverage.values()),
        max(sensor_map.values(), key=lambda x: x[0])[0] + max(sensor_coverage.values()),
    )

    for i in tqdm(range(min_x, max_x + 1)):
        loc = (i, Y)
        for k, v in sensor_coverage.items():
            if distance(loc, k) <= v:
                c += 1
                break

    beacons_in_row = {v for _, v in sensor_map.items() if v[1] == Y}
    return c - len(beacons_in_row)


dirs = [(1, -1), (-1, -1), (-1, 1), (1, 1)]


def part_2(sensor_map: dict[tuple[int, int], tuple[int, int]]) -> int:
    sensor_coverage = {k: distance(k, v) for k, v in sensor_map.items()}

    for sensor, radius in tqdm(sensor_coverage.items(), desc="sensors"):
        i = 0
        dir = dirs[i]
        p = (sensor[0], sensor[1] + radius + 1)

        while i < 4:
            # check if position covered by any beacons
            if 0 <= p[0] <= 4000000 and 0 <= p[1] <= 4000000:
                uncovered = True
                for k, v in sensor_coverage.items():
                    if distance(p, k) <= v:
                        uncovered = False
                        break
                if uncovered:
                    return p[0] * 4000000 + p[1]

            # continue around perimiter
            p = (p[0] + dir[0], p[1] + dir[1])

            if p[0] == sensor[0] or p[1] == sensor[1]:
                i += 1
                dir = dirs[i % 4]

    return 0


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
