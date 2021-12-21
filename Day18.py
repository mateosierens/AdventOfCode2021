from math import floor, ceil
from copy import deepcopy


class SnailNumber:
    def __init__(self, left, right, depth=0):
        self.left = left
        self.right = right
        self.depth = depth
        self.parent = None

    def find_explosion(self):
        if isinstance(self.left, SnailNumber):
            if self.left.depth < 4:
                explosion = self.left.find_explosion()
                if explosion is not None:
                    return explosion
            else:
                return self.left

        if isinstance(self.right, SnailNumber):
            if self.right.depth < 4:
                explosion = self.right.find_explosion()
                if explosion is not None:
                    return explosion
            else:
                return self.right
        return None

    def find_split(self):
        if isinstance(self.left, int):
            if self.left >= 10:
                return self
        else:
            split = self.left.find_split()
            if split is not None:
                return split

        if isinstance(self.right, int):
            if self.right >= 10:
                return self
        else:
            split = self.right.find_split()
            if split is not None:
                return split

        return None

    def update_left_neighbour(self, value):
        if self.parent is not None:
            if self is self.parent.right:
                if isinstance(self.parent.left, SnailNumber):
                    to_update = self.parent.left
                    while isinstance(to_update.right, SnailNumber):
                        to_update = to_update.right
                    to_update.right += value
                else:
                    self.parent.left += value
            else:
                to_update = self
                while to_update == to_update.parent.left:
                    to_update = to_update.parent
                    if to_update.parent is None:
                        return
                to_update = to_update.parent
                if isinstance(to_update.left, SnailNumber):
                    to_update = to_update.left
                    while isinstance(to_update.right, SnailNumber):
                        to_update = to_update.right
                    to_update.right += value
                else:
                    to_update.left += value

    def update_right_neighbour(self, value):
        if self.parent is not None:
            if self is self.parent.left:
                if isinstance(self.parent.right, SnailNumber):
                    to_update = self.parent.right
                    while isinstance(to_update.left, SnailNumber):
                        to_update = to_update.left
                    to_update.left += value
                else:
                    self.parent.right += value
            else:
                to_update = self
                while to_update == to_update.parent.right:
                    to_update = to_update.parent
                    if to_update.parent is None:
                        return
                to_update = to_update.parent
                if isinstance(to_update.right, SnailNumber):
                    to_update = to_update.right
                    while isinstance(to_update.left, SnailNumber):
                        to_update = to_update.left
                    to_update.left += value
                else:
                    to_update.right += value

    def update_depth(self):
        self.depth += 1
        if isinstance(self.left, SnailNumber):
            self.left.update_depth()
        if isinstance(self.right, SnailNumber):
            self.right.update_depth()

    def magnitude(self):
        left = 0
        right = 0
        if isinstance(self.left, SnailNumber):
            left += 3 * self.left.magnitude()
        else:
            left += 3 * self.left
        if isinstance(self.right, SnailNumber):
            right += 2 * self.right.magnitude()
        else:
            right += 2 * self.right
        return left + right


def parse_snail_number(line, depth=0):
    # if line starts with number, we have a value
    if line[0] != '[':
        return int(line)
    else:
        # find split between left and right part of snail number
        stack = []
        last_comma = -1
        for i, char in enumerate(line):
            if char == ',':
                stack.append(i)
            elif char == ']':
                last_comma = stack.pop()
        snail_number = SnailNumber(parse_snail_number(line[1:last_comma], depth + 1),
                                   parse_snail_number(line[last_comma + 1:-1], depth + 1))

        if isinstance(snail_number.left, SnailNumber):
            snail_number.left.parent = snail_number
        if isinstance(snail_number.right, SnailNumber):
            snail_number.right.parent = snail_number
        snail_number.depth = depth
        return snail_number


def read_input():
    snail_numbers = []
    with open("input18.txt") as f:
        for line in f:
            snail_numbers.append(parse_snail_number(line[:-1]))
    return snail_numbers


def explode(to_explode):
    to_explode.update_left_neighbour(to_explode.left)
    to_explode.update_right_neighbour(to_explode.right)

    if to_explode == to_explode.parent.left:
        to_explode.parent.left = 0
    else:
        to_explode.parent.right = 0


def split(to_split):
    if isinstance(to_split.left, int) and to_split.left >= 10:
        left = floor(to_split.left / 2)
        right = ceil(to_split.left / 2)
        to_split.left = SnailNumber(left, right, to_split.depth + 1)
        to_split.left.parent = to_split

    else:
        left = floor(to_split.right / 2)
        right = ceil(to_split.right / 2)
        to_split.right = SnailNumber(left, right, to_split.depth + 1)
        to_split.right.parent = to_split


def reduce(snail_number):
    reduced = False
    while not reduced:
        # check for explosion
        to_explode = snail_number.find_explosion()
        if to_explode is not None:
            explode(to_explode)
            continue
        # check for split
        to_split = snail_number.find_split()
        if to_split is not None:
            split(to_split)
            continue
        reduced = True
    return snail_number


def add_snail_numbers(snail1, snail2):
    snail1.update_depth()
    snail2.update_depth()
    add_snail = SnailNumber(snail1, snail2)
    snail1.parent = add_snail
    snail2.parent = add_snail
    return add_snail


def part1():
    snail_numbers = read_input()
    cur_number = snail_numbers[0]
    for i in range(1, len(snail_numbers)):
        addition = add_snail_numbers(cur_number, snail_numbers[i])
        cur_number = reduce(addition)
    return cur_number.magnitude()


def part2():
    magnitudes = []
    snail_numbers = read_input()
    for i in range(len(snail_numbers)):
        for j in range(len(snail_numbers)):
            if i != j:
                addition = add_snail_numbers(snail_numbers[i], snail_numbers[j])
                addition = reduce(addition)
                magnitudes.append(addition.magnitude())

                # restore snail_numbers
                snail_numbers = read_input()
    return max(magnitudes)

print(part2())