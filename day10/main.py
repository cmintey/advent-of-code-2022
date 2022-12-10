import os

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[str]:
    filepath = os.path.join(input_dir, filename)
    return open(filepath).read().strip().split("\n")


def part_1(input: list[str]) -> int:
    cycle = 0
    X = 1
    signals = []
    for instruction in input:
        cycle += 1

        if (cycle - 20) % 40 == 0:
            signals.append(cycle * X)

        if instruction != "noop":
            _, v = instruction.split(" ")
            cycle += 1

            if (cycle - 20) % 40 == 0:
                signals.append(cycle * X)

            X += int(v)

    return sum(signals)


def draw_px(cycle, X):
    px = ""
    if cycle % 40 in range(X, X + 3):
        px += "#"
    else:
        px += "."
    if cycle % 40 == 0:
        px += "\n"
    return px


def part_2(input: list[list[int]]) -> str:
    cycle = 1
    X = 1
    screen = ""
    for instruction in input:

        if instruction != "noop":
            _, v = instruction.split(" ")
            screen += draw_px(cycle, X)
            cycle += 1
            screen += draw_px(cycle, X)
            X += int(v)
            cycle += 1
        else:
            screen += draw_px(cycle, X)
            cycle += 1

    return screen


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
