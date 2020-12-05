import numpy as np


def read_file(input_path):
    with open(input_path, 'r') as f:
        lines = [elt.strip() for elt in f.readlines()]
    return lines


class Seat:
    def __init__(self, binary_partitioning_string):
        self.binary_partitioning_string = binary_partitioning_string
        self.row = None
        self.column = None
        self.id = None

    def get_row(self):
        row_string = self.binary_partitioning_string[:7]
        row_min, row_max = 0, 127
        for letter in row_string:
            if letter == 'F':
                row_max = (row_min + row_max) // 2
            else:
                row_min = ((row_min + row_max) // 2) + 1
        assert row_max == row_min
        self.row = row_max
        return row_max

    def get_column(self):
        column_string = self.binary_partitioning_string[7:]
        col_min, col_max = 0, 7
        for letter in column_string:
            if letter == 'L':
                col_max = (col_min + col_max) // 2
            else:
                col_min = ((col_min + col_max) // 2) + 1
        assert col_max == col_min
        self.column = col_max
        return col_max

    def get_seat_id(self):
        self.get_row()
        self.get_column()
        self.id = self.row * 8 + self.column
        return self.id


def find_missing_id(id_list):
    id_max = np.max(id_list)
    id_min = np.min(id_list)
    value_range = set(range(id_min, id_max))
    return set(value_range) - set(id_list)


def part1(input_list):
    max_id = -1
    for elt in input_list:
        s = Seat(elt)
        current_id = s.get_seat_id()
        if current_id > max_id:
            max_id = current_id
    return max_id


def part2(input_list):
    id_list = []
    for elt in input_list:
        s = Seat(elt)
        id_list.append(s.get_seat_id())
    return find_missing_id(id_list)


if __name__ == "__main__":
    path = read_file('input.txt')
    answer1 = part1(path)
    print(f'Part 1 answer is {answer1}')
    answer2 = part2(path)
    print(f'Part 2 answer is {answer2}')
