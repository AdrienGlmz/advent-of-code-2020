import numpy as np


class Password:
    def __init__(self, pwd, text_rule):
        numbers, character = text_rule.split(' ')
        character_min, character_max = numbers.split('-')
        self.pwd = pwd
        self.min = int(character_min)
        self.max = int(character_max)
        self.character = character
        self.character_count = None

    def is_valid_part1(self):
        character_count = np.sum([elt == self.character for elt in list(self.pwd)])
        self.character_count = character_count
        return (character_count >= self.min) and (character_count <= self.max)

    def is_valid_part2(self):
        pos1_check = (self.pwd[self.min - 1] == self.character)  # Removing 1 because indexing starts at 1
        pos2_check = (self.pwd[self.max - 1] == self.character)  # Removing 1 because indexing starts at 1
        return pos1_check != pos2_check


def read_file(path):
    with open(path, 'r') as f:
        input_list = f.readlines()
    processed_input_list = [tuple(elt.split(':')) for elt in input_list]
    return processed_input_list


def part1(input_list):
    valid_count = 0
    for rule, pwd in input_list:
        pwd_obj = Password(pwd.strip(), rule)
        valid_count += pwd_obj.is_valid_part1()
    return valid_count


def part2(input_list):
    valid_count = 0
    for rule, pwd in input_list:
        pwd_obj = Password(pwd.strip(), rule)
        valid_count += pwd_obj.is_valid_part2()
    return valid_count


if __name__ == "__main__":
    file_path = 'input.txt'
    inputs = read_file(file_path)
    answer_part1 = part1(inputs)
    print(f"Part 1 answer = {answer_part1}")
    answer_part2 = part2(inputs)
    print(f"Part 2 answer = {answer_part2}")
