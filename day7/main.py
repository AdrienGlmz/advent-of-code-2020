
def read_file(path):
    with open(path, 'r') as f:
        # remove special characters and final .
        lines = [elt.strip()[:-1] for elt in f.readlines()]
    return lines


def process_sentence(sentence):
    bag_name, children = sentence.split(' contain ')
    children_list = children.split(', ')
    if children_list == ['no other bags']:
        children_tuple_list = None
    else:
        children_tuple_list = [(int(elt[0]), ' '.join(elt[2:].split(' ')[:-1])) for elt in children_list]
    # Remove the 'bags' common word from the name
    bag_name = ' '.join(bag_name.split(' ')[:-1])
    return bag_name, children_tuple_list


def get_can_be_contained_by_dict(sentence_list):
    can_be_contained_by = dict()
    for line in sentence_list:
        parent, children = process_sentence(line)
        if children is not None:
            for qty, child in children:
                if can_be_contained_by.get(child):
                    can_be_contained_by[child].append(parent)
                else:
                    can_be_contained_by[child] = [parent]
    return can_be_contained_by


def get_contains_dict(sentence_list):
    contains = dict()
    for line in sentence_list:
        parent, children = process_sentence(line)
        contains[parent] = children
    return contains


def get_containers_rec(can_be_contained_by_dict, start_node='shiny gold'):
    parents_list = can_be_contained_by_dict.get(start_node)
    if parents_list is None:
        return set()
    else:
        return set(parents_list).union(*[get_containers_rec(can_be_contained_by_dict, parent) for parent in parents_list])


def get_nb_children_rec(contains_dict, start_node='shiny gold'):
    children = contains_dict[start_node]
    if children is None:
        return 0
    else:
        return sum([qty + qty * get_nb_children_rec(contains_dict, child) for qty, child in children])


if __name__ == "__main__":
    input_path = 'input.txt'
    l = read_file(input_path)
    d = get_can_be_contained_by_dict(l)
    answer1 = get_containers_rec(d)
    print(f"Part 1 answer is {len(answer1)}")
    d = get_contains_dict(l)
    answer2 = get_nb_children_rec(d)
    print(f"Part 2 answer is {answer2}")
