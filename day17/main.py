import os

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


# |0123456| 2
# |.......| 1
# +-------+
def simulate(jet_pattern: list[str], n_rocks: int):
    cave_width = 7
    cave_floor = 1
    height = 0
    rocks = set()
    seen = {}
    jet, n_jets = 0, len(jet_pattern)
    i = 0
    while i < n_rocks:
        rock = SHAPES[i % 5]
        y_pos = cave_floor + height + 3
        x_pos = 3 if (i % 5) == 1 else 2

        # logic courtesy of https://github.com/terminalmage/adventofcode/blob/main/2022/day17.py
        key = (i % 5, jet)
        if key in seen:
            seen_height, seen_rock_num = seen[key]
            cycle_length = i - seen_rock_num
            if i % cycle_length == n_rocks % cycle_length:
                cycle_height = height - seen_height
                rocks_remain = n_rocks - i
                cycles_remain = (rocks_remain // cycle_length) + 1
                return seen_height + (cycle_height * cycles_remain)
        else:
            seen[key] = (height, i)

        falling = True
        while falling:
            # jet motion
            motion = jet_pattern[jet]
            jet = (jet + 1) % n_jets
            if motion == "<":
                left_move = rock[2]((x_pos - 1, y_pos))
                # check for touching wall
                if all([x[0] >= 0 for x in left_move]):
                    # ceck for touching rock
                    if not left_move & rocks:
                        x_pos -= 1
            if motion == ">":
                right_move = rock[2]((x_pos + 1, y_pos))
                # check for touching wall
                if all([x[0] < cave_width for x in right_move]):
                    # check for touching rock
                    if not right_move & rocks:
                        x_pos += 1

            # drop one
            if y_pos - 1 >= cave_floor:
                # check for touching another rock
                if rock[2]((x_pos, y_pos - 1)) & rocks:
                    new_rocks = rock[2]((x_pos, y_pos))
                    rocks = rocks | new_rocks
                    height = max(height, max(new_rocks, key=lambda x: x[1])[1])
                    falling = False
                else:
                    y_pos -= 1
            else:
                new_rocks = rock[2]((x_pos, y_pos))
                rocks = rocks | new_rocks
                height = max(height, max(new_rocks, key=lambda x: x[1])[1])
                falling = False
        i += 1
    return height


def part_1(jet_pattern: list[str]) -> int:
    return simulate(jet_pattern, 2022)


def part_2(jet_pattern: list[str]) -> int:
    return simulate(jet_pattern, 1000000000000)


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
