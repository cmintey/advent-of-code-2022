from collections import defaultdict
import os

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> defaultdict[tuple[int, int], int]:
    filepath = os.path.join(input_dir, filename)
    lines = open(filepath).read().strip().split("\n")
    rocks = defaultdict(lambda: 0)
    for path in lines:
        coords = path.strip().split(" -> ")
        for i in range(1, len(coords)):
            [x1, y1] = map(int, coords[i - 1].split(","))
            [x2, y2] = map(int, coords[i].split(","))
            if x1 < x2:
                for x in range(x1, x2 + 1):
                    rocks[x, y1] = 1
            if x1 > x2:
                for x in range(x2, x1 + 1):
                    rocks[x, y1] = 1
            if y1 < y2:
                for y in range(y1, y2 + 1):
                    rocks[x1, y] = 1
            if y1 > y2:
                for y in range(y2, y1 + 1):
                    rocks[x1, y] = 1

    return rocks


def display(grid: defaultdict[tuple[int, int], int]):
    max_x = max(grid.keys(), key=lambda x: x[0])[0] + 1
    min_x = min(grid.keys(), key=lambda x: x[0])[0] - 1
    max_y = max(grid.keys(), key=lambda x: x[1])[1] + 2
    for y in range(0, max_y):
        for x in range(min_x, max_x + 1):
            if grid[(x, y)] == 1:
                print("#", end="")
            elif grid[(x, y)] == 2:
                print("o", end="")
            else:
                print(".", end="")
        print()


def part_1(cave: defaultdict[tuple[int, int], int]) -> int:
    void_y = max(cave.keys(), key=lambda x: x[1])[1] + 1
    sand = (500, 0)
    while True:
        if sand[1] >= void_y:
            break

        blocked = True
        for dx in [0, -1, 1]:
            if cave[(pos := (sand[0] + dx, sand[1] + 1))] == 0:
                sand = pos
                blocked = False
                break
        if blocked:
            cave[sand] = 2
            sand = (500, 0)

    return sum([1 for v in cave.values() if v == 2])


def part_2(rocks: defaultdict[tuple[int, int], int]) -> int:
    max_y = max(rocks.keys(), key=lambda x: x[1])[1] + 2

    sand = (500, 0)
    while True:
        if rocks[(500, 0)] == 2:
            break

        blocked = True
        for dx in [0, -1, 1]:
            if sand[1] + 1 == max_y:
                blocked = True
            elif rocks[(pos := (sand[0] + dx, sand[1] + 1))] == 0:
                sand = pos
                blocked = False

        if blocked:
            rocks[sand] = 2
            sand = (500, 0)

    return sum([1 for v in rocks.values() if v == 2])


input = parse_input("input.txt")
print(part_1(input))

input = parse_input("input.txt")
print(part_2(input))
