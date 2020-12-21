def read_file(path):
    with open(path, 'r') as f:
        lines = [elt.strip() for elt in f.readlines()]
    return lines


class Ship:
    def __init__(self, path):
        lines = read_file(path)
        self.instructions = lines
        self.direction = 0  # 0 means east
        self.pos_x = 0  # - west / east +
        self.pos_y = 0  # - south / north +

    def north(self, arg):
        self.pos_x += arg

    def south(self, arg):
        self.pos_x -= arg

    def east(self, arg):
        self.pos_y += arg

    def west(self, arg):
        self.pos_y -= arg

    def left(self, arg):
        self.direction = (self.direction - arg) % 360

    def right(self, arg):
        self.direction = (self.direction + arg) % 360

    def forward(self, arg):
        direction = self.direction
        if direction == 0:
            # east
            self.east(arg)
        elif direction == 90:
            # south
            self.south(arg)
        elif direction == 180:
            # west
            self.west(arg)
        else:
            assert direction == 270
            # north
            self.north(arg)

    def process_instructions(self):
        while self.instructions:
            instruction = self.instructions.pop(0)
            action, arg = instruction[0], int(instruction[1:])
            if action == 'N':
                self.north(arg)
            elif action == 'S':
                self.south(arg)
            elif action == 'W':
                self.west(arg)
            elif action == 'E':
                self.east(arg)
            elif action == 'R':
                self.right(arg)
                # print(f"After {instruction}, direction = {self.direction}")
            elif action == 'L':
                self.left(arg)
                # print(f"After {instruction}, direction = {self.direction}")
            else:
                assert action == 'F'
                self.forward(arg)
            # print(f"{instruction}\t x={self.pos_x}\t y={self.pos_y}")

    def get_manhattan_distance(self):
        print(f"x = {self.pos_x} \t y = {self.pos_y}")
        return abs(self.pos_x) + abs(self.pos_y)


class ShipPart2(Ship):
    def __init__(self, input_path):
        super(ShipPart2, self).__init__(input_path)
        self.waypoint_x = 10  # - west / east +
        self.waypoint_y = 1  # - south / north +

    def north(self, arg):
        self.waypoint_y += arg

    def south(self, arg):
        self.waypoint_y -= arg

    def east(self, arg):
        self.waypoint_x += arg

    def west(self, arg):
        self.waypoint_x -= arg

    def right(self, arg):
        arg = arg % 360
        x, y = self.waypoint_x, self.waypoint_y
        if arg == 90:
            self.waypoint_x = y
            self.waypoint_y = -x
        if arg == 180:
            self.waypoint_x = -x
            self.waypoint_y = -y
        if arg == 270:
            self.waypoint_x = -y
            self.waypoint_y = x

    def left(self, arg):
        self.right(- arg)

    def forward(self, arg):
        self.pos_x += self.waypoint_x * arg
        self.pos_y += self.waypoint_y * arg
        print(f"New position = {self.pos_x} \t {self.pos_y}")


if __name__ == "__main__":
    input_path = 'input.txt'
    ship = Ship(input_path)
    ship.process_instructions()
    answer1 = ship.get_manhattan_distance()
    print(f"Part 1 answer is {answer1}")
    ship = ShipPart2(input_path)
    ship.process_instructions()
    answer2 = ship.get_manhattan_distance()
    print(f"Part 2 answer is {answer2}")
