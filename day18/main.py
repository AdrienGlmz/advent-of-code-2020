from math import prod
from more_itertools import chunked


def read_file(path):
    with open(path, 'r') as f:
        lines = [elt.strip() for elt in f.readlines()]
    return lines


def analyse(s, calc):
    if "(" not in s:
        return calc(s)

    res = {}
    stack = []

    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)
        elif c == ")":
            res[stack.pop()] = i

    a, b = next(iter(res.items()))
    e = analyse(s[a+1: b], calc)
    return analyse(f"{s[:a]}{e}{s[b+1:]}", calc)


def calc_part1(exp):
    s = exp.split()
    res = int(s[0])
    for operation, nb in chunked(s[1:], 2):
        if operation == "+":
            res += int(nb)
        elif operation == "*":
            res *= int(nb)
    return res


def calc_part2(exp):
    k = exp.split('*')
    return prod(calc_part1(elt) for elt in k)


if __name__ == "__main__":
    input_path = "input.txt"
    lines = read_file(input_path)
    answer1 = sum([analyse(elt, calc_part1) for elt in lines])
    print(f"Part 1 answer is {answer1}")
    answer2 = sum([analyse(elt, calc_part2) for elt in lines])
    print(f"Part 2 answer is {answer2}")
