import numpy as np


class Map:
    def __init__(self, lines, initial_pos=(0, 0)):
        lines = np.array([list(elt) for elt in lines])
        lines = np.where(lines == '#', 1, 0)
        self.map = lines
        self.x = initial_pos[0]
        self.y = initial_pos[1]
        self.current_state = self.map[self.x, self.y]
        self.done = False

    def move(self, direction_x, direction_y):
        self.x += direction_x
        self.y = (self.y + direction_y) % self.map.shape[1]
        self.done = (self.x >= (self.map.shape[0] - 1))
        self.current_state = self.map[self.x, self.y]

    def reset(self):
        self.x = 0
        self.y = 0
        self.current_state = self.map[0, 0]
        self.done = False


def read_file(path):
    with open(path, 'r') as f:
        lines = [elt.strip() for elt in f.readlines()]
    return lines


def part1(map_object: Map, strategy=(1, 3)):
    tree_count = 0
    while not map_object.done:
        direction_x, direction_y = strategy[0], strategy[1]
        map_object.move(direction_x, direction_y)
        tree_count += map_object.current_state
    return tree_count


def part2(map_object: Map, strategy_list):
    tree_count = []
    for strategy in strategy_list:
        map_object.reset()
        tree_count.append(part1(map_object, strategy=strategy))
    return np.product(tree_count)


if __name__ == "__main__":
    file_path = 'input.txt'
    input_lines = read_file(file_path)
    m = Map(input_lines)
    tree_count_part1 = part1(m)
    print(f"Part 1 answer = {tree_count_part1}")
    tree_count_part2 = part2(m, [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)])
    print(f"Part 2 answer = {tree_count_part2}")
