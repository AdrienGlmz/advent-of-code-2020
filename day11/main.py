import numpy as np


def read_file(path):
    with open(path, 'r') as f:
        rows = [list(elt.strip()) for elt in f.readlines()]
    return np.array(rows)


class Seats:
    def __init__(self, path):
        rows = read_file(path)
        self.current_state = rows
        self.is_stable = False
        self.update_count = 0

    def number_of_occupied_adjacent_seat(self, seat_idx):
        max_dim0, max_dim1 = self.current_state.shape[0] - 1, self.current_state.shape[1] - 1
        if seat_idx[0] == 0 and seat_idx[1] == 0:
            # Top left corner
            adjacent_indices = [(0, 1), (1, 0), (1, 1)]
        elif seat_idx[0] == 0 and seat_idx[1] == max_dim1:
            # Top right corner
            adjacent_indices = [(0, max_dim1 - 1), (1, max_dim1), (1, max_dim1 - 1)]
        elif seat_idx[0] == max_dim0 and seat_idx[1] == 0:
            # Bottom left corner
            adjacent_indices = [(max_dim0 - 1, 0), (max_dim0, 1), (max_dim0 - 1, 1)]
        elif seat_idx[0] == max_dim0 and seat_idx[1] == max_dim1:
            # Bottom right corner
            adjacent_indices = [(max_dim0, max_dim1 - 1), (max_dim0 - 1, max_dim1), (max_dim0 - 1, max_dim1 - 1)]
        elif seat_idx[0] == 0:
            # First row but not in corners
            adjacent_indices = [(0, seat_idx[1] - 1), (0, seat_idx[1] + 1), (1, seat_idx[1] - 1), (1, seat_idx[1]),
                                (1, seat_idx[1] + 1)]
        elif seat_idx[0] == max_dim0:
            # Last row but not in corners
            adjacent_indices = [(max_dim0, seat_idx[1] - 1), (max_dim0, seat_idx[1] + 1),
                                (max_dim0 - 1, seat_idx[1] - 1), (max_dim0 - 1, seat_idx[1]),
                                (max_dim0 - 1, seat_idx[1] + 1)]
        elif seat_idx[1] == 0:
            # First column but not in corners
            adjacent_indices = [(seat_idx[0] - 1, 0), (seat_idx[0] - 1, 1), (seat_idx[0], 1), (seat_idx[0] + 1, 1),
                                (seat_idx[0] + 1, 0)]
        elif seat_idx[1] == max_dim1:
            # Last column but not in corners
            adjacent_indices = [(seat_idx[0] - 1, max_dim1), (seat_idx[0] - 1, max_dim1 - 1),
                                (seat_idx[0], max_dim1 - 1), (seat_idx[0] + 1, max_dim1 - 1),
                                (seat_idx[0] + 1, max_dim1)]
        else:
            x = seat_idx[0]
            y = seat_idx[1]
            adjacent_indices = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                                (x, y - 1), (x, y + 1),
                                (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        return sum([self.current_state[idx] == '#' for idx in adjacent_indices])

    def update_part1(self):
        new_state = []
        current_state = self.current_state
        for i in range(current_state.shape[0]):
            new_row = []
            for j in range(current_state.shape[1]):
                occupied_seats = self.number_of_occupied_adjacent_seat([i, j])
                if current_state[i, j] == 'L' and occupied_seats == 0:
                    new_row.append('#')
                elif current_state[i, j] == '#' and occupied_seats >= 4:
                    new_row.append('L')
                else:
                    new_row.append(current_state[i, j])
            new_state.append(new_row)
        new_state = np.array(new_state)
        if (new_state == current_state).all():
            self.is_stable = True
        else:
            self.update_count += 1
            self.current_state = new_state

    def get_to_stable_state(self, part1=True):
        while not self.is_stable:
            if part1:
                self.update_part1()
            else:
                self.update_part2()

    def get_nb_seat_occupied(self):
        return sum(sum([elt == '#' for elt in self.current_state]))

    def part1(self):
        self.get_to_stable_state()
        return self.get_nb_seat_occupied()

    def find_nearest_seat(self, current_seat, direction):
        current_state = self.current_state
        direction = np.array(direction)
        next_seat = np.array(current_seat) + direction
        max_dim0, max_dim1 = self.current_state.shape[0] - 1, self.current_state.shape[1] - 1
        boundary_condition = (next_seat[0] >= 0) and (next_seat[0] <= max_dim0) and \
                             (next_seat[1] >= 0) and (next_seat[1] <= max_dim1)
        while boundary_condition:
            if current_state[tuple(next_seat)] != '.':
                # Return 1 if occupied else 0
                return 1 if current_state[tuple(next_seat)] == '#' else 0
            next_seat = next_seat + direction
            boundary_condition = (next_seat[0] >= 0) and (next_seat[0] <= max_dim0) and \
                                 (next_seat[1] >= 0) and (next_seat[1] <= max_dim1)
        return 0

    def update_part2(self):
        new_state = []
        current_state = self.current_state
        for i in range(current_state.shape[0]):
            new_row = []
            for j in range(current_state.shape[1]):
                directions = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 1), (0, 1), (1, 1), (-1, 0)]
                occupied_seats = sum([self.find_nearest_seat((i, j), elt) for elt in directions])
                if current_state[i, j] == 'L' and occupied_seats == 0:
                    new_row.append('#')
                elif current_state[i, j] == '#' and occupied_seats >= 5:
                    new_row.append('L')
                else:
                    new_row.append(current_state[i, j])
            new_state.append(new_row)
        new_state = np.array(new_state)
        if (new_state == current_state).all():
            self.is_stable = True
        else:
            self.update_count += 1
            self.current_state = new_state

    def part2(self):
        self.get_to_stable_state(part1=False)
        return self.get_nb_seat_occupied()


if __name__ == '__main__':
    input_path = 'input.txt'
    seats = Seats(input_path)
    answer1 = seats.part1()
    print(f"Part1 answer is {answer1}")
    seats = Seats(input_path)
    answer2 = seats.part2()
    print(f"Part2 answer is {answer2}")
