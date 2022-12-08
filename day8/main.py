import os
import numpy as np

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> str:
    filepath = os.path.join(input_dir, filename)
    grid = []
    with open(filepath, "r") as f:
        for line in f:
            row = list(map(int, list(line.strip())))
            grid.append(row)
    return grid


def perimiter(length: int, width: int) -> int:
    return (length * 2) + (width * 2) - 4


def gridify(grid: list[list[int]]):
    new_grid = np.zeros((len(grid), len(grid[0])), dtype=int)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            new_grid[i, j] = grid[i][j]
    return new_grid


def part_1(input: list[list[int]]) -> int:
    grid = gridify(input)
    vis = perimiter(*grid.shape)
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            t = grid[i, j]
            left, right = grid[i, :j], grid[i, j + 1 :]
            up, down = grid[:i, j], grid[i + 1 :, j]
            if (
                t > np.max(left)
                or t > np.max(right)
                or t > np.max(up)
                or t > np.max(down)
            ):
                vis += 1

    return vis


def scan_ahead(ahead, height) -> int:
    score = 0
    for x in ahead:
        if x < height:
            score += 1
        elif x >= height:
            score += 1
            break
    return score


def scan_behind(behind, height) -> int:
    score = 0
    for i in range(1, len(behind) + 1):
        x = behind[-i]
        if x < height:
            score += 1
        elif x >= height:
            score += 1
            break
    return score


def part_2(input: list[list[int]]) -> int:
    grid = gridify(input)
    scenic_score = 0
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            score = 1

            t = grid[i, j]
            left, right = grid[i, :j], grid[i, j + 1 :]
            up, down = grid[:i, j], grid[i + 1 :, j]
            score *= scan_behind(left, t)
            score *= scan_ahead(right, t)
            score *= scan_behind(up, t)
            score *= scan_ahead(down, t)

            if score > scenic_score:
                scenic_score = score

    return scenic_score


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
