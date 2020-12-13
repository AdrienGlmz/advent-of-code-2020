from itertools import product
import numpy as np

def read_file(path):
    with open(path, 'r') as f:
        l = [int(elt.strip()) for elt in f.readlines()]
    return l


def get_set_previous(idx, full_list, ref_length):
    first_idx = idx - ref_length
    sub_list = full_list[first_idx:idx]
    return [elt1 + elt2 for elt1, elt2 in product(sub_list, sub_list) if elt1 != elt2]


class XMAS:
    def __init__(self, path, ref_length=25):
        self.input = read_file(path)
        self.end_line = len(self.input)
        self.ref_length = ref_length
        self.is_valid = None

    def first_number_breaking_rule(self):
        # Start at 26th position
        for idx in range(self.ref_length, self.end_line):
            valid_set = get_set_previous(idx, self.input, self.ref_length)
            if self.input[idx] not in valid_set:
                self.is_valid = False
                return self.input[idx]

    def find_continuous_sum(self, target, window):
        lists_to_consider = [self.input]
        for _ in range(window - 1):
            last_iteration = lists_to_consider[-1]
            lists_to_consider.append([0] + last_iteration)
        possible_sums = [list(elt) for elt in zip(*lists_to_consider)]
        for l in possible_sums:
            if np.sum(l) == target:
                small, large = np.min(l), np.max(l)
                return small + large
        return False

    def part2(self, target):
        window = 2
        found = False
        while not found:
            print(window)
            found = self.find_continuous_sum(target=target, window=window)
            window += 1
        return found


if __name__ == "__main__":
    input_path = 'input.txt'
    xmas = XMAS(input_path)
    answer1 = xmas.first_number_breaking_rule()
    print(f"Part 1 answer is {answer1}")
    answer2 = xmas.part2(answer1)
    print(f"Part 2 answer is {answer2}")
