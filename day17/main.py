from itertools import product
import numpy as np


def read_file(path):
    with open(path, 'r') as f:
        lines = [elt.strip() for elt in f.readlines()]
    return lines


def process_initial_state(lines, dim=3):
    initial_state = dict()
    for y, row in enumerate(lines):
        for x, cube in enumerate(row):
            if dim == 3:
                # consider we are at z = 0
                initial_state[(x, y, 0)] = cube
            else:
                # consider we are at z = 0 and w = 0
                initial_state[(x, y, 0, 0)] = cube
    return initial_state


class ConwayCubes:
    def __init__(self, path, n_dim=3):
        lines = read_file(path)
        initial_state = process_initial_state(lines, dim=n_dim)
        self.current_state = initial_state
        self.current_cycle = 0
        self.dim = n_dim

    def get_active_neighbors_number(self, cube_idx):
        if self.dim == 3:
            neighbors = list(product(*[(-1, 0, 1)]*3))
            # don't want to consider the current index
            neighbors.remove((0, 0, 0))
        else:
            assert self.dim == 4
            neighbors = list(product(*[(-1, 0, 1)] * 4))
            neighbors.remove((0, 0, 0, 0))
        neighbors = np.array(neighbors) + [cube_idx]
        active_count = sum([self.current_state.get(tuple(n)) == '#' for n in neighbors])
        return active_count

    def get_set_of_neighbors(self):
        active_cubes = list(self.current_state.keys())
        neighbors_set = set()
        for c in active_cubes:
            if self.dim == 3:
                neighbors = list(product(*[(-1, 0, 1)] * 3))
            else:
                neighbors = list(product(*[(-1, 0, 1)] * 4))
            neighbors = np.array(neighbors) + [c]
            neighbors_set = neighbors_set.union([tuple(elt) for elt in neighbors])
        return neighbors_set

    def next_cycle(self):
        next_state = dict()
        neighbors_to_consider = list(self.get_set_of_neighbors())
        for current_cube in neighbors_to_consider:
            active_neighbors = self.get_active_neighbors_number(current_cube)
            if self.current_state.get(current_cube) == '#':
                if active_neighbors in [2, 3]:
                    next_state[current_cube] = '#'
                else:
                    next_state[current_cube] = '.'
            if self.current_state.get(current_cube) == '.' or self.current_state.get(current_cube) is None:
                if active_neighbors == 3:
                    next_state[current_cube] = '#'
                else:
                    next_state[current_cube] = '.'
        self.current_state = next_state
        self.current_cycle += 1

    def main(self):
        while self.current_cycle < 6:
            self.next_cycle()
        active_cubes = sum([elt == '#' for _, elt in self.current_state.items()])
        return active_cubes


if __name__ == "__main__":
    input_path = 'input.txt'
    c = ConwayCubes(input_path)
    answer1 = c.main()
    print(f"Part 1 answer is {answer1}")
    c = ConwayCubes(input_path, n_dim=4)
    answer2 = c.main()
    print(f"Part 2 answer is {answer2}")
