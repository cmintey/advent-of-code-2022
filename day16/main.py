import os
import re
from collections import deque
from tqdm import tqdm

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[list[str]]:
    filepath = os.path.join(input_dir, filename)
    lines = open(filepath).read().strip().split("\n")
    valves = []
    for line in lines:
        r = re.findall(r"[A-Z]{2}|\d+", line)
        valves.append(r)

    return valves


class Valve:
    def __init__(self, name: str, flow_rate=0) -> None:
        self.name = name
        self.flow_rate = flow_rate
        self.is_open = False
        self.tunnels: list["Valve"] = []

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, __o: "Valve") -> bool:
        return self.name == __o.name

    def __hash__(self) -> int:
        return self.name.__hash__()


def create_valves(raw_valves: list[list[str]]) -> dict[str, Valve]:
    valves: dict[str, Valve] = {}
    for raw_valve in raw_valves:
        valve = Valve(raw_valve[0], int(raw_valve[1]))
        valves[raw_valve[0]] = valve
    for raw_valve in raw_valves:
        valve = valves[raw_valve[0]]
        for connection in raw_valve[2:]:
            conn = valves.get(connection)
            valve.tunnels.append(conn)
    return valves


def bfs(root: Valve):
    reachable: dict[str, int] = {}
    visited = set()
    queue = deque()
    queue.append((root, 0))
    while len(queue) > 0:
        cur, depth = queue.popleft()
        visited.add(cur)
        for n in cur.tunnels:
            if n not in visited:
                reachable[n.name] = depth + 1
                queue.append((n, depth + 1))

    return reachable


def create_costs(valves: dict[str, Valve]) -> dict[str, dict[str, int]]:
    costs: dict[str, dict[str, int]] = {}
    for v, valve in valves.items():
        reachable = bfs(valve)
        costs[v] = reachable
    return costs


def find_pressures(valves: dict[str, Valve], costs: dict[str, dict[str, int]], t: int):
    pressures = []
    paths = []
    stack = [(t, 0, ["AA"])]
    while len(stack) > 0:
        t_rem, p, path = stack.pop()

        pressures.append(p)
        paths.append(path)

        cur = path[-1]
        targets = [
            v
            for _, v in valves.items()
            if v.flow_rate > 0 and not v.is_open and v.name not in path
        ]
        if targets == []:
            pressures.append(p)
            paths.append(path)

        for target in targets:
            cost = costs[cur][target.name]
            if (new_t := t_rem - cost - 1) < 0:
                pressures.append(p)
                paths.append(path)
            else:
                new_path = [x for x in path]
                new_path.append(target.name)
                stack.append((new_t, p + (target.flow_rate * new_t), new_path))

    return pressures, paths


def part_1(raw_valves: list[list[str]]) -> int:
    valves = create_valves(raw_valves)
    costs = create_costs(valves)
    pressures, _ = find_pressures(valves, costs, 30)
    return max(pressures)


def part_2(raw_valves: list[list[str]]) -> int:
    valves = create_valves(raw_valves)
    costs = create_costs(valves)
    x = list(zip(*find_pressures(valves, costs, 26)))
    p, paths = zip(*sorted(x, reverse=True))
    path_sets = [set(path[1:]) for path in paths]

    i, j = 0, 1
    while path_sets[i] & path_sets[j]:
        j += 1

    best = p[i] + p[j]
    max_j = j
    print(max_j)

    for i in tqdm(range(1, max_j)):
        for j in range(i + 1, max_j + 1):
            if not path_sets[i] & path_sets[j]:
                best = max(best, p[i] + p[j])

    return best


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
