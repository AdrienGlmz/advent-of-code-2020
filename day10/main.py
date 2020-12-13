import numpy as np


def read_file(path):
    with open(path, 'r') as f:
        lines = set(int(elt.strip()) for elt in f.readlines())
    return lines


class Adapters:
    def __init__(self, path):
        self.adapters_set = read_file(path)
        self.differences = None
        self.adapters_seen = set()
        self.current_voltage = 0

    @staticmethod
    def get_working_adapters(adapters_to_consider, current_voltage):
        return [adpt for adpt in adapters_to_consider if (adpt - current_voltage) <= 3]

    def get_next_difference(self):
        remaining_adapters = self.adapters_set - self.adapters_seen
        working_adapters = self.get_working_adapters(remaining_adapters, self.current_voltage)
        next_adapter = min(working_adapters)
        next_difference = next_adapter - self.current_voltage
        self.current_voltage = next_adapter
        self.adapters_seen = self.adapters_seen.union([next_adapter])
        return next_difference

    def get_number_arrangement(self):
        dp = [1]
        # dp will hold how many combinations can be used with ith adapter
        adapters_list = [0] + sorted(list(self.adapters_set))
        for i in range(1, len(adapters_list)):
            current_sum = 0
            for j in range(i):
                if adapters_list[j] + 3 >= adapters_list[i]:
                    current_sum += dp[j]
            dp.append(current_sum)
        return dp

    def part1(self):
        differences_list = []
        while self.adapters_set != self.adapters_seen:
            differences_list.append(self.get_next_difference())
        differences_list = np.array(differences_list)
        differences_distribution = {1: 0, 2: 0, 3: 0}
        for diff in differences_distribution.keys():
            differences_distribution[diff] = sum(differences_list == diff)
        # because of built-in adapter
        differences_distribution[3] += 1
        return differences_distribution[3] * differences_distribution[1]

    def part2(self):
        return self.get_number_arrangement()[-1]


if __name__ == "__main__":
    input_path = 'input.txt'
    adapters = Adapters(input_path)
    answer1 = adapters.part1()
    print(f"Part 1 answer is {answer1}")
    answer2 = adapters.part2()
    print(f"Part 2 answer is {answer2}")
