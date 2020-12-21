import numpy as np


def read_file(path):
    with open(path, 'r') as f:
        timestamp = f.readline().strip()
        buses = f.readline().strip().split(',')
    return int(timestamp), buses


def earliest_bus_possible(timestamp, buses):
    valid_buses = [int(elt) for elt in buses if elt != 'x']
    wait_time = [(bus, - (timestamp % bus) + bus) for bus in valid_buses]
    wait_time = sorted(wait_time, key=lambda x: x[1])
    return wait_time


def part1(path):
    timestamp, buses = read_file(path)
    wait_time = earliest_bus_possible(timestamp, buses)
    bus, wait = wait_time[0]
    return bus * wait


def find_requirements(buses):
    return [(int(bus), idx) for idx, bus in enumerate(buses) if bus != 'x']


def part2(path):
    """
    This is the chinese remainder theorem: find x such that x = a1 (mod n1) ... x = aK (mod nK) with n1, ..., nK
    pairwise coprime
    This function is using this page's notations: https://fr.wikipedia.org/wiki/Théorème_des_restes_chinois
    """
    _, buses = read_file(path)
    requirements = find_requirements(buses)
    # Transform (bus, idx) to (bus, - idx % bus) to prepare for algorithm
    # This means x = - 1 (mod 13) <=> x = 12 (mod 13)
    requirements = [(bus, -idx % bus) for bus, idx in requirements]
    # Bus -> prime integer = prime_int
    # idx -> remainder = remain
    N = np.prod([prime_int for prime_int, _ in requirements])
    solution = 0
    for prime_int, remain in requirements:
        n_hat = N / prime_int
        pgcd, u, v = extended_euclidian(prime_int, n_hat)
        assert pgcd == 1
        # make sure that v is positive
        v = v % prime_int
        e = int(n_hat * v)
        solution += remain * e
    # Return minimum solution
    return solution % N


def extended_euclidian(a, b):
    """
    Extended euclidian algorithm that given a, b return u, v such that au + bv = 1 and PGCD(a, b)
    :param a: int
    :param b: int
    :return: (r = PGCD(a, b), u, v)
    """
    r, u, v, r_p, u_p, v_p = a, 1, 0, b, 0, 1
    while r_p != 0:
        q = r // r_p
        r, u, v, r_p, u_p, v_p = r_p, u_p, v_p, r - q * r_p, u - q*u_p, v - q * v_p
    return r, u, v


if __name__ == "__main__":
    input_path = 'input.txt'
    t, b = read_file(input_path)
    answer1 = part1(input_path)
    print(f"Part 1 answer is {answer1}")
    answer2 = part2(input_path)
    print(f"Part 2 answer is {answer2}")
