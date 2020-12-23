def read_file(path):
    with open(path, 'r') as f:
        lines = ''.join(f.readlines())
    requirements, my_ticket, other_tickets = lines.split('\n\n')
    requirements = [elt.strip() for elt in requirements.split('\n')]
    my_ticket = [elt.strip() for elt in my_ticket.split('\n')[1:]]
    other_tickets = [elt.strip() for elt in other_tickets.split('\n')[1:]]
    return requirements, my_ticket, other_tickets


def reject_invalid_tickets(requirements, other_tickets):
    # Process requirements
    possible_values = set()
    for r in requirements:
        name, values = r.split(': ')
        values1, values2 = values.split(' or ')
        min1, max1 = values1.split('-')
        min2, max2 = values2.split('-')
        possible_values = possible_values.union(range(int(min1), int(max1) + 1))
        possible_values = possible_values.union(range(int(min2), int(max2) + 1))

    # Check if ticket is valid
    error_rate = 0
    is_valid_list = []
    for idx, ticket in enumerate(other_tickets):
        is_valid = True
        values = [int(elt) for elt in ticket.split(',')]
        for v in values:
            if v not in possible_values:
                is_valid = False
                error_rate += v
        if is_valid:
            is_valid_list.append(idx)
    return error_rate, is_valid_list


def match_field_name(requirements, is_valid_list, other_tickets):
    # Process requirements
    fields_requirements = dict()
    for r in requirements:
        name, values = r.split(': ')
        values1, values2 = values.split(' or ')
        min1, max1 = values1.split('-')
        min2, max2 = values2.split('-')
        fields_requirements[name] = set().union(range(int(min1), int(max1) + 1)).union(range(int(min2), int(max2) + 1))

    n_cols = len(fields_requirements.keys())
    attribution_possibilities = {k: [] for k in fields_requirements.keys()}
    # list all possible column values for each possible field name
    for i in range(n_cols):
        field_values = set()
        for idx, ticket in enumerate(other_tickets):
            if idx in is_valid_list:
                field_values.add(int(ticket.split(',')[i]))
        attribution_list = [i]
        for field_name, possible_values in fields_requirements.items():
            attribution_list.append(field_values.issubset(possible_values))
            if field_values.issubset(possible_values):
                attribution_possibilities[field_name].append(i)

    # Deduce the only possible combination that works for all fields
    field_name_matching = {k: None for k in fields_requirements.keys()}
    while len(attribution_possibilities.keys()) > 1:
        tuple_list = sorted(attribution_possibilities.items(), key=lambda x: len(x[1]))
        first_field, col_list = tuple_list[0][0], tuple_list[0][1]
        if len(col_list) != 1:
            raise AssertionError("Can't do attribution...")
        else:
            field_name_matching[first_field] = col_list[0]
        # Remove this col and field from the list of possibilities
        attribution_possibilities.pop(first_field)
        # Remove this col from all the columns
        attribution_possibilities = {k: [elt for elt in v if elt != col_list[0]]
                                     for k, v in attribution_possibilities.items()}
    return field_name_matching


def part2(requirements, my_ticket, other_tickets):
    _, is_valid = reject_invalid_tickets(requirements, other_tickets)
    field_name_matching = match_field_name(requirements, is_valid, other_tickets)
    fields_to_keep = ['departure location', 'departure station', 'departure platform',
                      'departure track', 'departure date', 'departure time']
    my_ticket = [int(elt) for elt in my_ticket[0].split(',')]
    prod = 1
    for f in fields_to_keep:
        idx = field_name_matching[f]
        prod *= my_ticket[idx]
    return prod


if __name__ == "__main__":
    input_path = 'input.txt'
    r, m, o = read_file(input_path)
    answer1, is_valid = reject_invalid_tickets(r, o)
    print(f"Part 1 answer is {answer1}")
    answer2 = part2(r, m, o)
    print(f"Part 2 answer is {answer2}")
