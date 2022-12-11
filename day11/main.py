from functools import reduce
import os
import re
import math

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_input(filename: str) -> list[str]:
    filepath = os.path.join(input_dir, filename)
    return open(filepath).read().strip().split("\n\n")


class Monkey:
    def __init__(
        self, id: int, items=[], operation=None, mod=0, true=0, false=0
    ) -> None:
        self.id: int = id
        self.items: list[int] = items
        self.operation = operation
        self.factor = 0
        self.test: int = mod
        self.monkey_true: int = true
        self.monkey_false: int = false
        self.inspections: int = 0

    def __repr__(self) -> str:
        s = f"Monkey {self.id}:\n"
        s += f"  Items: {self.items}\n"
        s += f"  Operation: {self.operation}\n"
        s += f"  Test: divisible by {self.mod}\n"
        s += f"    If true: throw to monkey {self.monkey_true}\n"
        s += f"    If false: throw to monkey {self.monkey_false}\n"
        return s

    def take_turn(self, monkeys: list["Monkey"], part=1, mod=None) -> None:
        for i in range(len(self.items)):
            f = self.items[i] if self.factor == "old" else int(self.factor)
            self.items[i] = self.operation(self.items[i], f)
            if part == 1:
                self.items[i] = self.items[i] // 3
            if part == 2:
                self.items[i] = self.items[i] % mod
            if self.items[i] % self.test == 0:
                # throw to self.monkey_true
                monkeys[self.monkey_true].items.append(self.items[i])
            else:
                # throw to self.monkey_false
                monkeys[self.monkey_false].items.append(self.items[i])

            self.inspections += 1
        self.items = []


OPS = {
    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y,
    "-": lambda x, y: x - y,
    "/": lambda x, y: x / y,
}


def parse_monkey(raw_monkey: str) -> Monkey:
    monkey_parts = raw_monkey.splitlines()
    monkey: Monkey
    for part in monkey_parts:
        if part.startswith("Monkey"):
            id = re.findall(r"\d+", part.strip())[0]
            monkey = Monkey(int(id))
        if part.strip().startswith("Starting items"):
            items = part.strip().split(":")
            monkey.items = list(map(int, items[1].strip().split(", ")))
        if part.strip().startswith("Operation"):
            operation = part.strip().split(":")
            op_parts = operation[1].strip().split(" ")
            monkey.operation = OPS[op_parts[-2]]
            monkey.factor = op_parts[-1]
        if part.strip().startswith("Test"):
            mod = re.findall(r"\d+", part.strip())[0]
            monkey.test = int(mod)
        if part.strip().startswith("If true"):
            true = re.findall(r"\d+", part.strip())[0]
            monkey.monkey_true = int(true)
        if part.strip().startswith("If false"):
            false = re.findall(r"\d+", part.strip())[0]
            monkey.monkey_false = int(false)

    return monkey


def part_1(input: list[str], rounds: int) -> int:
    monkeys = [parse_monkey(raw) for raw in input]
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.take_turn(monkeys, part=1)
    inspections = sorted([m.inspections for m in monkeys])
    return math.prod(inspections[-2:])


def part_2(input: list[str], rounds: int) -> int:
    monkeys = [parse_monkey(raw) for raw in input]
    mod = reduce(lambda x, y: x * y.test, monkeys, 1)
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.take_turn(monkeys, part=2, mod=mod)
    inspections = sorted([m.inspections for m in monkeys])
    return math.prod(inspections[-2:])


input = parse_input("input.txt")
print(part_1(input, 20))
print(part_2(input, 10000))
