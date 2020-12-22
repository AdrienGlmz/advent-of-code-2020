from itertools import product


def read_file(path):
    with open(path, 'r') as f:
        lines = [elt.strip() for elt in f.readlines()]
    return lines


def get_bin(x, n=36):
    return format(x, 'b').zfill(n)


def get_int(b):
    return int(b, 2)


def get_possibilities(position_bin):
    """
    Return all the possible int with a binary string '000110XX01X0'. X denotes unknown bits
    """
    possibilites = []
    nb_of_unkown = sum(elt == 'X' for elt in list(position_bin))
    for elt in product(*[[0, 1]]*nb_of_unkown):
        tuple_idx = 0
        possibility = list(position_bin)
        for i in range(len(possibility)):
            if possibility[i] == 'X':
                possibility[i] = str(elt[tuple_idx])
                tuple_idx += 1
        possibilites.append(get_int(''.join(possibility)))
    return possibilites


class Bitmask:
    def __init__(self, path):
        lines = read_file(path)
        self.instructions = lines
        self.bitmask = ''
        self.memory = {0: get_bin(0)}

    def update_mask(self, new_mask):
        self.bitmask = new_mask

    def update_mem_part1(self, position, value):
        # Get 32-bit binary
        value = get_bin(value)
        # Overwrite with bitmask
        value_list = list(value)
        for i in range(len(list(self.bitmask))):
            if self.bitmask[i] != 'X':
                value_list[i] = self.bitmask[i]
        # Write in mem
        self.memory[position] = ''.join(value_list)

    def update_mem_part2(self, position, value):
        # Get 32-bit binary
        value = get_bin(value)
        # Overwrite with bitmask
        position_bin = list(get_bin(position))
        for i in range(len(list(self.bitmask))):
            if self.bitmask[i] != '0':
                position_bin[i] = self.bitmask[i]
        positions = get_possibilities(''.join(position_bin))
        # Write in mem
        for position in positions:
            self.memory[position] = ''.join(value)

    def get_memory_sum(self):
        return sum([get_int(v) for k, v in self.memory.items()])

    def process_instructions(self, part1=True):
        while self.instructions:
            next_instructions = self.instructions.pop(0)
            command, arg = next_instructions.split(' = ')
            if command == 'mask':
                self.update_mask(arg)
            else:
                position = int(command.split('[')[1][:-1])
                if part1:
                    self.update_mem_part1(position, int(arg))
                else:
                    self.update_mem_part2(position, int(arg))

    def part1(self):
        self.process_instructions()
        return self.get_memory_sum()

    def part2(self):
        self.process_instructions(part1=False)
        return self.get_memory_sum()


if __name__ == "__main__":
    input_path = 'input.txt'
    bitmask = Bitmask(input_path)
    answer1 = bitmask.part1()
    print(f"Part 1 answer is {answer1}")
    a = get_possibilities('00000000000000000000000000000001X0XX')
    bitmask = Bitmask(input_path)
    answer2 = bitmask.part2()
    print(f"Part 2 answer is {answer2}")
