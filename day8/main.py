def read_file(path):
    with open(path, 'r') as f:
        lines = [elt.strip().split(' ') for elt in f.readlines()]
        lines = [(operation, int(arg)) for operation, arg in lines]
    return lines


class Program:
    def __init__(self, file_path):
        lines = read_file(file_path)
        self.file_path = file_path
        self.instructions = lines
        self.accumulator = 0
        self.current_index = 0
        self.end = False
        self.max_index = len(lines)
        # Part of the check for infinite loop
        self.visited_index = None
        self.infinite_loop = None

    def reset(self):
        lines = read_file(self.file_path)
        self.instructions = lines
        self.accumulator = 0
        self.current_index = 0
        self.end = False
        self.max_index = len(lines)

    def acc(self, arg):
        self.accumulator += arg
        self.current_index += 1

    def jmp(self, arg):
        self.current_index += arg

    def nop(self, arg):
        self.current_index += 1

    def execute(self, operation, arg):
        if operation == 'acc':
            self.acc(arg)
        elif operation == 'jmp':
            self.jmp(arg)
        else:
            self.nop(arg)

    def check_for_infinite_loop(self):
        """
        Check for infinite loop in the program
        :return: accumulator value before an instruction would be run a second time
                 if there is no infinite loop, return False
        """
        visited_index = []
        while not self.end:
            if self.current_index in visited_index:
                if not self.infinite_loop and not self.visited_index:
                    # If it's the first time invoking the method
                    self.visited_index = visited_index
                return self.accumulator
            else:
                visited_index.append(self.current_index)
                operation, arg = self.instructions[self.current_index]
                self.execute(operation, arg)
            if self.current_index == self.max_index:
                self.end = True
                print("Program ended successfully")
                return False

    def find_corrected_program(self):
        """
        Check for one modification that would make the program run without infinite loop
        :return: accumulator value at the end of the program if ran until the end
                 False if no way to remove infinite loo[
        """
        self.current_index = 0
        self.check_for_infinite_loop()
        index_list_to_inspect = self.visited_index
        for idx in reversed(index_list_to_inspect):
            self.reset()
            operation, arg = self.instructions[idx]
            if operation in ['jmp', 'nop']:
                new_operation = 'nop' if operation == 'jmp' else 'jmp'
                # try updating instructions
                self.instructions[idx] = new_operation, arg
                if not self.check_for_infinite_loop():
                    print(f"By replacing index {idx} from '{operation}' to '{new_operation}', program was successful")
                    return self.accumulator
        return False


if __name__ == "__main__":
    input_path = 'input.txt'
    p = Program(input_path)
    answer1 = p.check_for_infinite_loop()
    print(f"Part 1 answer is  {answer1}")
    answer2 = p.find_corrected_program()
    print(f"Part 2 answer is {answer2}")
