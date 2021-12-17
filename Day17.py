from math import inf


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def read_input():
    with open("input17.txt") as f:
        split = f.readline().split()
        x_range = [int(x) for x in split[2][2:-1].split('..')]
        y_range = [int(y) for y in split[3][2:].split('..')]
        return x_range, y_range


def step(pos: Coord, velocity):
    pos.x += velocity[0]
    pos.y += velocity[1]

    new_x_vel = velocity[0]
    if velocity[0] != 0:
        new_x_vel = velocity[0] - (velocity[0] // abs(velocity[0]))  # + 1 or - 1 depending on x velocity sign
    new_y_vel = velocity[1] - 1

    return pos, (new_x_vel, new_y_vel)


def shot_eval(cur_step, target):
    """
    :returns
    0: not yet there
    1: hit
    2: miss
    """
    x_range = (target[0][0], target[0][1])
    y_range = (target[1][0], target[1][1])

    if x_range[0] <= cur_step.x <= x_range[1] and y_range[0] <= cur_step.y <= y_range[1]:
        return 1
    elif x_range[1] < cur_step.x or y_range[0] > cur_step.y:
        return 2
    else:
        return 0


def find_highest_shot(target):
    # naive method
    hits = []
    for i in range(0, target[0][1] * 2):
        for j in range(target[1][0], abs(target[1][0])):
            velocity = (i, j)
            pos = Coord(0, 0)
            highest_y = -inf
            while True:
                pos, velocity = step(pos, velocity)
                if pos.y > highest_y:
                    highest_y = pos.y
                score = shot_eval(pos, target)
                if score == 1:
                    hits.append(highest_y)
                    break
                elif score == 2:
                    break
    highest_y = max(hits)
    return highest_y


def find_hitting_shots(target):
    # naive method
    hits = []
    for i in range(0, target[0][1] * 2):
        for j in range(target[1][0], abs(target[1][0])):
            initial_velocity = (i, j)
            velocity = (i, j)
            pos = Coord(0, 0)
            while True:
                pos, velocity = step(pos, velocity)
                score = shot_eval(pos, target)
                if score == 1:
                    hits.append(initial_velocity)
                    break
                elif score == 2:
                    break
    return len(hits)

def part1():
    target = read_input()
    return find_highest_shot(target)

def part2():
    target = read_input()
    return find_hitting_shots(target)

print(part2())
