import os

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[str]:
    filepath = os.path.join(input_dir, filename)
    return open(filepath).read().strip().split("\n")


def distance(x: tuple[int, int], y: tuple[int, int]) -> int:
    return max(abs(y[0] - x[0]), abs(y[1] - x[1]))


def clamp(x: int, val: int) -> int:
    return max(-val, min(val, x))


def direction(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return (clamp(y[0] - x[0], 1), clamp(y[1] - x[1], 1))


DMAP = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}


def simulate(num_knots: int, moves: list[str]) -> int:
    visited = set()
    knots = [(0, 0) for _ in range(num_knots)]
    visited.add((0, 0))
    for move in moves:
        print(f"== {move} ==")
        dir, steps = move.split(" ")
        for _ in range(int(steps)):
            knots[0] = (knots[0][0] + DMAP[dir][0], knots[0][1] + DMAP[dir][1])

            for i in range(1, len(knots)):
                dist = distance(knots[i - 1], knots[i])
                if dist == 2:
                    direct = direction(knots[i], knots[i - 1])
                    knots[i] = (knots[i][0] + direct[0], knots[i][1] + direct[1])
            visited.add(knots[-1])

    return len(visited)


def part_1(input: list[str]) -> int:
    return simulate(2, input)


def part_2(input: list[list[int]]) -> int:
    return simulate(10, input)


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
