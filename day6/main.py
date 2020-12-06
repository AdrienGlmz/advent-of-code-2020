import re


def read_file(path):
    with open(path, 'r') as f:
        # split per group
        lines = ''.join(f.readlines()).split('\n\n')
        # remove \n characters
        lines = [re.findall(r'[a-z]+', group) for group in lines]
    return lines


def answer_per_group_or(group_answers):
    distinct_yes = set(''.join(group_answers))
    return len(distinct_yes)


def answer_per_group_and(group_answers):
    answer_set = [set(answers) for answers in group_answers]
    return len(set.intersection(*answer_set))


def part1(all_answers):
    return sum([answer_per_group_or(group) for group in all_answers])


def part2(all_answers):
    return sum([answer_per_group_and(group) for group in all_answers])


if __name__ == "__main__":
    input_path = 'input.txt'
    answers_list = read_file(input_path)
    answer1 = part1(answers_list)
    print(f"Part1 answer is {answer1}")
    answer2 = part2(answers_list)
    print(f"Part2 answer is {answer2}")
