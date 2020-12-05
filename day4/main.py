import re


def read_file(path):
    with open(path, 'r') as f:
        single_lines = ''.join(f.readlines())
        passport_lines = single_lines.split('\n\n')
    return passport_lines


class Passport:
    def __init__(self, passport_string):
        fields = [elt for elt in re.split(' |\n', passport_string) if elt]
        fields_dict = dict()
        for field in fields:
            key, value = field.split(':')
            fields_dict[key] = value
        self.byr = fields_dict.get('byr', False)
        self.iyr = fields_dict.get('iyr', False)
        self.eyr = fields_dict.get('eyr', False)
        self.hgt = fields_dict.get('hgt', False)
        self.hcl = fields_dict.get('hcl', False)
        self.ecl = fields_dict.get('ecl', False)
        self.pid = fields_dict.get('pid', False)
        self.cid = fields_dict.get('cid', False)

    # def is_valid(self):
    #     return (bool(self.byr) and bool(self.iyr) and bool(self.eyr) and bool(self.hgt) and bool(self.hcl)
    #             and bool(self.ecl) and bool(self.pid) and bool(self.cid))

    def is_north_pole_credentials(self):
        return (bool(self.byr) and bool(self.iyr) and bool(self.eyr) and bool(self.hgt) and bool(self.hcl)
                and bool(self.ecl) and bool(self.pid))

    def byr_valid(self):
        byr = int(self.byr)
        cond = (1920 <= byr <= 2002) and (len(list(str(self.byr))) == 4)
        return cond

    def iyr_valid(self):
        iyr = int(self.iyr)
        cond = (2010 <= iyr <= 2020) and (len(list(str(self.iyr))) == 4)
        return cond

    def eyr_valid(self):
        eyr = int(self.eyr)
        cond = (2020 <= eyr <= 2030) and (len(list(str(self.eyr))) == 4)
        return cond

    def hgt_valid(self):
        numbers = int(''.join(re.findall(r'\d', self.hgt)))
        unit = ''.join(re.findall(r'[a-z]', self.hgt))
        if unit == 'cm':
            cond = 150 <= numbers <= 193
        elif unit == 'in':
            cond = 59 <= numbers <= 76
        else:
            cond = False
        return cond

    def hcl_valid(self):
        hex_part = re.findall(r'[a-f0-9]', self.hcl)
        return (self.hcl[0] == '#') and len(hex_part) == 6

    def ecl_valid(self):
        valid_options = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        return self.ecl in valid_options

    def pid_valid(self):
        numbers = re.findall(r'\d', self.pid)
        return len(numbers) == 9

    def is_valid(self):
        return (self.byr_valid() and self.iyr_valid() and self.eyr_valid() and self.hgt_valid() and self.hcl_valid()
                and self.ecl_valid() and self.pid_valid())


def part1(passport_list):
    count_valid = 0
    for elt in passport_list:
        p = Passport(elt)
        count_valid += int(p.is_north_pole_credentials())
    return count_valid


def part2(passport_list):
    count_valid = 0
    for elt in passport_list:
        p = Passport(elt)
        count_valid += int(p.is_north_pole_credentials() and p.is_valid())
    return count_valid


if __name__ == "__main__":
    file_path = 'input.txt'
    input_list = read_file(file_path)
    answer1 = part1(input_list)
    print(f"Answer 1 = {answer1}")
    answer2 = part2(input_list)
    print(f"Answer 2 = {answer2}")
