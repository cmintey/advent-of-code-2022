from functools import cmp_to_key
import os

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[list[str]]:
    filepath = os.path.join(input_dir, filename)
    lines = open(filepath).read().strip().split("\n")
    rocks = set()
    for path in lines:
        coords = path.strip().split(" -> ")
        for i in range(1, len(coords)):
            [x1, y1] = map(int, coords[i - 1].split(","))
            [x2, y2] = map(int, coords[i].split(","))
            if x1 < x2:
                rocks.update(zip(range(x1, x2 + 1), [y1] * (1 + x2 - x1)))
            if x1 > x2:
                rocks.update(zip(range(x2, x1 + 1), [y1] * (1 + x1 - x2)))
            if y1 < y2:
                rocks.update(zip([x1] * (1 + y2 - y1), range(y1, y2 + 1)))
            if y1 > y2:
                rocks.update(zip([x1] * (1 + y1 - y2), range(y2, y1 + 1)))

    return rocks


def display(rocks, sand_spaces):
    max_x = max(rocks | sand_spaces, key=lambda x: x[0])[0] + 1
    min_x = min(rocks | sand_spaces, key=lambda x: x[0])[0] - 1
    max_y = max(rocks, key=lambda x: x[1])[1] + 2
    for y in range(0, max_y):
        for x in range(min_x, max_x + 1):
            if (x, y) in rocks:
                print("#", end="")
            elif (x, y) in sand_spaces:
                print("o", end="")
            else:
                print(".", end="")
        print()


def part_1(rocks: set[tuple[int, int]]) -> int:
    void_y = max(rocks, key=lambda x: x[1])[1] + 1
    space_available = True
    sand_spaces = set()
    sand = None
    while space_available:
        if not sand:
            sand = (500, 1)

        if sand[1] >= void_y:
            break

        if (pos := (sand[0], sand[1] + 1)) not in rocks | sand_spaces:
            sand = pos
        elif (pos := (sand[0] - 1, sand[1] + 1)) not in rocks | sand_spaces:
            sand = pos
        elif (pos := (sand[0] + 1, sand[1] + 1)) not in rocks | sand_spaces:
            sand = pos
        else:
            sand_spaces.add(sand)
            sand = None
    display(rocks, sand_spaces)
    return len(sand_spaces)


def part_2(rocks: set[tuple[int, int]]) -> int:
    # max_x = max(rocks, key=lambda x: x[0])[0] + 1000
    # min_x = min(rocks, key=lambda x: x[0])[0] - 100
    max_y = max(rocks, key=lambda x: x[1])[1] + 2
    # rocks.update(zip(range(min_x, max_x), [max_y] * (1 + max_x - min_x)))

    sand_spaces = set()
    sand = None
    i = 0
    while True:
        if (i % 1000) == 0:
            print(f"{i} steps taken")

        if not sand:
            sand = (500, 0)

        if sand[1] + 1 == max_y:
            sand_spaces.add(sand)
            sand = None
            continue

        if (pos := (sand[0], sand[1] + 1)) not in rocks | sand_spaces:
            sand = pos
        elif (pos := (sand[0] - 1, sand[1] + 1)) not in rocks | sand_spaces:
            sand = pos
        elif (pos := (sand[0] + 1, sand[1] + 1)) not in rocks | sand_spaces:
            sand = pos
        else:
            sand_spaces.add(sand)
            sand = None

        if (500, 0) in sand_spaces:
            break

        i += 1
    display(rocks, sand_spaces)
    return len(sand_spaces)


input = parse_input("input.txt")
print(part_1(input))
print()
print(part_2(input))
