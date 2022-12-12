import os

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[list[str]]:
    filepath = os.path.join(input_dir, filename)
    return [list(s) for s in open(filepath).read().strip().split("\n")]


def get_cost(letter):
    l = "a" if letter == "S" else "z" if letter == "E" else letter
    return ord(l) - 97


def find_next(costs: list[list[int]], visited):
    smallest = 100000
    loc = None
    for i in range(len(costs)):
        for j in range(len(costs[0])):
            if costs[i][j] < smallest and (i, j) not in visited:
                smallest = costs[i][j]
                loc = (i, j)

    return loc


def part_1(input: list[list[str]]) -> int:
    costs = [[100000 for _ in range(len(input[0]))] for _ in range(len(input))]
    visited = set()
    start = end = (0, 0)
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == "S":
                start = (i, j)
                costs[i][j] = 0
            elif input[i][j] == "E":
                end = (i, j)

    cur = start
    while end not in visited:
        i, j = cur[0], cur[1]
        if i - 1 >= 0:
            c = get_cost(input[i - 1][j])
            if c - get_cost(input[i][j]) <= 1:
                costs[i - 1][j] = min(costs[i - 1][j], costs[i][j] + 1)
        if i + 1 < len(costs):
            c = get_cost(input[i + 1][j])
            if c - get_cost(input[i][j]) <= 1:
                costs[i + 1][j] = min(costs[i + 1][j], costs[i][j] + 1)
        if j - 1 >= 0:
            c = get_cost(input[i][j - 1])
            if c - get_cost(input[i][j]) <= 1:
                costs[i][j - 1] = min(costs[i][j - 1], costs[i][j] + 1)
        if j + 1 < len(costs[0]):
            c = get_cost(input[i][j + 1])
            if c - get_cost(input[i][j]) <= 1:
                costs[i][j + 1] = min(costs[i][j + 1], costs[i][j] + 1)

        visited.add(cur)
        cur = find_next(costs, visited)
    return costs[end[0]][end[1]]


def part_2(input: list[list[str]]) -> int:
    costs = [[100000 for _ in range(len(input[0]))] for _ in range(len(input))]
    visited = set()
    end = (0, 0)
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == "E":
                end = (i, j)
                costs[i][j] = 0

    cur = end
    while get_cost(input[cur[0]][cur[1]]) != 0:
        i, j = cur[0], cur[1]
        if i - 1 >= 0:
            c = get_cost(input[i - 1][j])
            if get_cost(input[i][j]) - c <= 1:
                costs[i - 1][j] = min(costs[i - 1][j], costs[i][j] + 1)
        if i + 1 < len(costs):
            c = get_cost(input[i + 1][j])
            if get_cost(input[i][j]) - c <= 1:
                costs[i + 1][j] = min(costs[i + 1][j], costs[i][j] + 1)
        if j - 1 >= 0:
            c = get_cost(input[i][j - 1])
            if get_cost(input[i][j]) - c <= 1:
                costs[i][j - 1] = min(costs[i][j - 1], costs[i][j] + 1)
        if j + 1 < len(costs[0]):
            c = get_cost(input[i][j + 1])
            if get_cost(input[i][j]) - c <= 1:
                costs[i][j + 1] = min(costs[i][j + 1], costs[i][j] + 1)

        visited.add(cur)
        cur = find_next(costs, visited)
    return costs[cur[0]][cur[1]]


input = parse_input("input.txt")
# print(part_1(input))
print(part_1(input))
print(part_2(input))
