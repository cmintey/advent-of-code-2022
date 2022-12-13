from functools import cmp_to_key
import os

input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input/")


def parse_list(list_str: str) -> list:
    l = None
    i = 0
    while i < len(list_str):
        c = list_str[i]
        if c == "[":
            if l is None:
                l = []
            else:
                ret, end = parse_list(list_str[i:])
                l.append(ret)
                i += end
        elif c == "]":
            return (l, i)
        elif c != "," and c != "]":
            try:
                l.append(int(list_str[i : i + 2]))
                i += 1
            except:
                l.append(int(c))
        i += 1

    return l, len(list_str)


def parse_input(filename: str) -> list[list[str]]:
    filepath = os.path.join(input_dir, filename)
    pairs = open(filepath).read().strip().split("\n\n")
    lists = []
    for pair in pairs:
        [first, second] = pair.split("\n")
        lists.append(parse_list(first)[0])
        lists.append(parse_list(second)[0])

    return lists


def compare(left, right):
    match left, right:
        case int(), int():
            return left - right
        case list(), list():
            for l, r in zip(left, right):
                if diff := compare(l, r):
                    return diff
            return len(left) - len(right)
        case int(), list():
            return compare([left], right)
        case list(), int():
            return compare(left, [right])


def part_1(input: list[list]) -> int:
    s = 0
    for i in range(0, len(input), 2):
        first, second = input[i], input[i + 1]
        res = compare(first, second)
        if res < 0:
            s += (i // 2) + 1
    return s


DIVIDER_PKTS = [[[2]], [[6]]]


def part_2(input: list[list[str]]) -> int:
    input.extend(DIVIDER_PKTS)
    pkts = sorted(input, key=cmp_to_key(compare))
    decoder_key = 1
    for i, pkt in enumerate(pkts):
        if pkt in DIVIDER_PKTS:
            decoder_key *= i + 1
    return decoder_key


input = parse_input("input.txt")
print(part_1(input))
print(part_2(input))
