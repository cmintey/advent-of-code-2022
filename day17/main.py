import os
import re
from tqdm import tqdm

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[str]:
    filepath = os.path.join(input_dir, filename)
    return list(open(filepath).read().strip())


# width x height
# from bottom left-most point
SHAPES = [
    (3, 0, lambda a: set([(a[0] + i, a[1]) for i in range(4)])),  # -
    (
        1,
        2,
        lambda a: set([(a[0], a[1] + i) for i in range(3)])
        | set([(a[0] + i, a[1] + 1) for i in range(-1, 2)]),
    ),  # +
    (
        2,
        2,
        lambda a: set([(i, a[1]) for i in range(a[0], a[0] + 3)])
        | set([(a[0] + 2, j) for j in range(a[1], a[1] + 3)]),
    ),  # _|
    (0, 3, lambda a: set([(a[0], j) for j in range(a[1], a[1] + 4)])),  # |
    (
        1,
        1,
        lambda a: set(
            [(i, j) for i in range(a[0], a[0] + 2) for j in range(a[1], a[1] + 2)]
        ),
    ),  # box
]


def display(rocks, height):
    for i in range(height + 1, 0, -1):
        print("|", end="")
        for j in range(0, 7):
            if (j, i) in rocks:
                print("#", end="")
            else:
                print(".", end="")
        print("|")
    print("+-------+")


DEBUG = False

# |0123456| 2
# |.......| 1
# +-------+
def part_1(jet_pattern: list[str]) -> int:
    cave_width = 7
    cave_floor = 1
    height = 0
    rocks = set()
    jet, n_jets = 0, len(jet_pattern)
    for i in range(2022):
        if DEBUG:
            print("rock", i)
        rock = SHAPES[i % 5]
        y_pos = cave_floor + height + 3
        x_pos = 3 if (i % 5) == 1 else 2
        falling = True
        while falling:
            if DEBUG:
                print("x, y", x_pos, y_pos)
            # jet motion
            motion = jet_pattern[jet]
            jet = (jet + 1) % n_jets
            if motion == "<":
                if DEBUG:
                    print("try left")
                left_move = rock[2]((x_pos - 1, y_pos))
                if DEBUG:
                    print(left_move)
                # if x_pos - 1 >= 0:
                if all([x[0] >= 0 for x in left_move]):
                    if left_move & rocks:
                        if DEBUG:
                            print("  blocked by rock")
                    else:
                        if DEBUG:
                            print(" success")
                        x_pos -= 1
            if motion == ">":
                if DEBUG:
                    print(f"try right")
                right_move = rock[2]((x_pos + 1, y_pos))
                if DEBUG:
                    print(right_move)
                if all([x[0] < cave_width for x in right_move]):
                    if right_move & rocks:
                        if DEBUG:
                            print("  blocked by rock")
                    else:
                        if DEBUG:
                            print("  success")
                        x_pos += 1
            if DEBUG:
                print("x", x_pos)

            if DEBUG:
                print("go down")
            # drop one
            if y_pos - 1 >= cave_floor:
                # if touching another rock
                if rock[2]((x_pos, y_pos - 1)) & rocks:
                    new_rocks = rock[2]((x_pos, y_pos))
                    rocks = rocks | new_rocks
                    height = max(height, max(new_rocks, key=lambda x: x[1])[1])
                    if DEBUG:
                        print("  blocked by rock")
                    falling = False
                # rocks.append; break;
                else:
                    if DEBUG:
                        print("  success")
                    y_pos -= 1
            else:
                if DEBUG:
                    print("  hit ground")
                # rocks.append()
                new_rocks = rock[2]((x_pos, y_pos))
                rocks = rocks | new_rocks
                height = max(height, max(new_rocks, key=lambda x: x[1])[1])
                falling = False
            if DEBUG:
                print("x, y", x_pos, y_pos)
        if DEBUG:
            print(rocks)
        if DEBUG:
            display(rocks, height)
        if DEBUG:
            print(height)
        if DEBUG:
            print()
    # display(rocks, height)
    # print(rocks)
    return height


def part_2(sensor_map: dict[tuple[int, int], tuple[int, int]]) -> int:
    pass


input = parse_input("input.txt")
print(part_1(input))
# print(part_2(input))
