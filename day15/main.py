def read_file(path):
    with open(path, 'r') as f:
        start_numbers = [int(elt) for elt in f.readline().strip().split(',')]
    return start_numbers


class MemoryGame:
    def __init__(self, path):
        starting_numbers = read_file(path)
        self.history = starting_numbers
        # will hold number already seen as {n1: k1}
        # where n1 is the number and k1 is the last turn where the number was used
        self.numbers_seen = {n: [idx + 1] for idx, n in enumerate(starting_numbers)}

    def next_turn(self):
        last_number_played = self.history[-1]
        current_turn_idx = len(self.history) + 1
        if self.numbers_seen.get(last_number_played) is None or len(self.numbers_seen.get(last_number_played)) == 1:
            # we haven't seen the number before or the last time was the first time spoken
            # then the number spoken for this round is 0
            self.history.append(0)
            if self.numbers_seen.get(0):
                self.numbers_seen[0].append(current_turn_idx)
            else:
                self.numbers_seen[0] = [current_turn_idx]
        else:
            # the number has been spoken before
            # we need to compute the difference between this turn and the last time the number was spoken
            last_time_spoken = self.numbers_seen.get(last_number_played)[-2]
            turn_difference = (current_turn_idx - 1) - last_time_spoken
            # we announce turn_difference and store it into the dict of numbers seen
            self.history.append(turn_difference)
            if self.numbers_seen.get(turn_difference):
                self.numbers_seen[turn_difference].append(current_turn_idx)
            else:
                self.numbers_seen[turn_difference] = [current_turn_idx]

    def part1(self):
        while len(self.history) <= 2019:
            self.next_turn()
        # return 2020 - 1 because the first turn is turn 1
        return self.history[2019]

    def part2(self):
        while len(self.history) <= (30000000 - 1):
            self.next_turn()
        return self.history[30000000 - 1]


if __name__ == "__main__":
    input_path = 'input.txt'
    game = MemoryGame(input_path)
    answer1 = game.part1()
    print(f"Part 1 answer is {answer1}")
    answer2 = game.part2()
    print(f"Part 2 answer is {answer2}")
