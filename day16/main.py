import math
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


def find_pressures2(valves: dict[str, Valve], costs: dict[str, dict[str, int]], t: int):
    pressures = []
    paths = []
    stack = [(t, 0, ["AA"], ["AA"])]
    # stack = [((t, 0, ["AA"]), (t, 0, ["AA"]))]
    while len(stack) > 0:
        t_rem, p, path, e_path = stack.pop()

        # human goes first
        cur = path[-1]
        e_cur = e_path[-1]
        targets = [
            v
            for _, v in valves.items()
            if v.flow_rate > 0
            and not v.is_open
            and v.name not in path
            and v.name not in e_path
        ]
        if targets == []:
            pressures.append(p)
            paths.append(path)

        for target1 in targets:
            for target2 in targets:
                if target1 == target2:
                    continue

                cost1 = costs[cur][target1.name]
                cost2 = costs[e_cur][target2.name]
                if (new_t := t_rem - max(cost1, cost2) - 1) < 0:
                    pressures.append(p)
                    paths.append(path)
                else:
                    new_path1 = [x for x in path]
                    new_path2 = [x for x in e_path]

                    new_path1.append(target1.name)
                    new_path2.append(target2.name)
                    new_p = (
                        p
                        + (target1.flow_rate * (t_rem - cost1 - 1))
                        + (target2.flow_rate * (t_rem - cost2 - 1))
                    )
                    stack.append((new_t, new_p, new_path1, new_path2))

    return pressures, paths


def part_2_(raw_valves: list[list[str]]) -> int:
    valves = create_valves(raw_valves)
    costs = create_costs(valves)
    p, _ = find_pressures2(valves, costs, 26)
    print(max(p))


def part_2(raw_valves: list[list[str]]) -> int:
    valves = create_valves(raw_valves)
    costs = create_costs(valves)
    x = list(zip(*find_pressures(valves, costs, 26)))
    p, paths = zip(*sorted(x, reverse=True))
    print(paths[0])

    best = 0
    # j_max = j
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            si = set(paths[i])
            sj = set(paths[j])
            print(si, sj, si & sj)
            # if not (inter := (set(paths[i]) & set(paths[j]))):
            #     print("here")
            #     best = max(best, p[i] + p[j])
            # print(inter)

    return best

    # for i in range(1, len(paths)):
    #     for j in range(i + 1, len(paths)):
    #         if any(x in paths[j] for x in paths[i]):
    #             continue
    #         best = max(best, p[i] + p[j])
    # return best
    # pressures, paths = find_pressures(valves, costs, 26)
    # best = 0
    # d = []
    # pps = sorted(zip(pressures, paths), reverse=True)
    # for i in range(len(pps)):
    #     for j in range(i + 1, len(pps)):
    #         unique = True
    #         for x in zip(pps[i][1][1:], pps[j][1][1:]):
    #             # print(x)
    #             if x[0] == x[1]:
    #                 unique = False
    #                 break
    #         # if any(x in pps[j][1][1:] for x in pps[i][1][1:]):
    #         #     continue

    #         if unique:
    #             best = max(best, pps[i][0] + pps[j][0])
    #             d.append(best)
    # print(d)
    # return best

    # pressures, paths = sorted(zip(pressures, paths), reverse=True)
    # print(pressures)
    # return max(pressures)


input = parse_input("example.txt")
# print(part_1(input))
print(part_1(input))

print(part_2(input))
