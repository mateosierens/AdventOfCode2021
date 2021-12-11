from math import inf

def read_input():
    with open("input7.txt") as f:
        line = f.readline()
        return [int(pos) for pos in line.split(',')]

def fuel_cost(h_pos, positions):
    return sum([abs(h_pos - pos) for pos in positions])

def inflated_fuel_cost(h_pos, positions):
    original = [abs(h_pos - pos) for pos in positions]
    return sum([sum([i for i in range(cost + 1)]) for cost in original])

def get_closest(positions, function=fuel_cost):
    # naive way: iterate over every possible position
    best_cost = inf
    best_pos = -1
    biggest_position = max(positions)
    for i in range(biggest_position + 1):
        cost = function(i, positions)
        if cost < best_cost:
            best_cost = cost
            best_pos = i
    return best_pos, best_cost

def part1():
    positions = read_input()
    h_pos, cost = get_closest(positions)
    return cost

def part2():
    positions = read_input()
    h_pos, cost = get_closest(positions, inflated_fuel_cost)
    return cost

print(part2())