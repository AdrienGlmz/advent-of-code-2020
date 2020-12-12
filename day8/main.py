def read_file(path):
    with open(path, 'r') as f:
        lines = [elt.strip().split(' ') for elt in f.readlines()]
        lines = [(operation, int(arg)) for operation, arg in lines]
    return lines


class Program:
    def __init__(self, file_path):
        lines = read_file(file_path)
        self.instructions = lines
        self.accumulator = 0
        self.current_index = 0
        self.infinite_loop = None
        self.index_to_switch = None
        self.end = False
        self.max_index = len(lines)

    def acc(self, arg):
        self.accumulator += arg
        self.current_index += 1

    def jmp(self, arg):
        self.current_index += arg

    def nop(self, arg):
        self.current_index += 1

    def check_for_infinite_loop(self):
        visited_index = []
        while not self.end:
            if self.current_index in visited_index:
                print(visited_index)
                self.infinite_loop = self.accumulator
                self.index_to_switch = visited_index[-1]
                break
            else:
                visited_index.append(self.current_index)
                operation, arg = self.instructions[self.current_index]
                if operation == 'acc':
                    self.acc(arg)
                elif operation == 'jmp':
                    self.jmp(arg)
                else:
                    self.nop(arg)

    def run_corrected_program(self):
        self.current_index = 0
        while self.current_index < self.max_index:
            operation, arg = self.instructions[self.current_index]
            if self.current_index != self.index_to_switch:
                if operation == 'acc':
                    self.acc(arg)
                elif operation == 'jmp':
                    self.jmp(arg)
                else:
                    self.nop(arg)
            else:
                print("ok")
                if operation == 'acc':
                    self.acc(arg)
                elif operation == 'jmp':
                    self.nop(arg)
                else:
                    self.jmp(arg)
        return self.accumulator


if __name__ == "__main__":
    input_path = 'input_test.txt'
    p = Program(input_path)
    p.check_for_infinite_loop()
    print(f"Part 1 answer is {p.infinite_loop}")
    print(f"Index to switch is {p.index_to_switch}")
    answer2 = p.run_corrected_program()
    print(f"Part 2 answer is {answer2}")
