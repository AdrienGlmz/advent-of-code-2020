import numpy as np
import time


def read_file(path):
    with open(path, 'r') as f:
        input_list = [int(elt.strip()) for elt in f.readlines()]
    return input_list


def time_it(func, *args):
    start_time = time.time()
    value = func(*args)
    duration = time.time() - start_time
    print(f"In {duration:.4f} seconds: Answer of {func.__name__} is {value}")


def check_sum(n1, n2, n3=0, sum_to_achieve=2020):
    return (n1 + n2 + n3) == sum_to_achieve


def part1(input_list):
    value = np.nan
    for n1 in input_list:
        for n2 in input_list:
            if check_sum(n1, n2):
                value = n1 * n2
                return value
    return value


def part2(input_list):
    value = np.nan
    for n1 in input_list:
        for n2 in input_list:
            for n3 in input_list:
                if check_sum(n1, n2, n3):
                    value = n1 * n2 * n3
                    return value
    return value


def part2_opt(input_list, target=2020):
    input_list = sorted(input_list, reverse=True)
    value = np.nan
    for n1 in input_list:
        if n1 > target:
            continue
        for n2 in input_list:
            if n1 + n2 > target:
                continue
            for n3 in input_list:
                if n1 + n2 + n3 > target:
                    continue
                if check_sum(n1, n2, n3):
                    value = n1 * n2 * n3
                    return value
    return value


if __name__ == "__main__":
    file_path = 'input.txt'
    input_values = read_file(file_path)

    time_it(part1, input_values)
    time_it(part2, input_values)
    time_it(part2_opt, input_values)
