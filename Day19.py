from math import radians, sin, cos
from itertools import combinations_with_replacement, permutations
from copy import deepcopy


class Scanner:
    def __init__(self, id):
        self.id = id
        self.beacons = []
        self.abs_coord = None

    def all_orientations(self):
        scanners = [Scanner(self.id) for _ in range(120)]
        for beacon in self.beacons:
            index = 0
            for configuration in combinations_with_replacement([0, 1, 2, 3], 3):
                for perm in permutations(configuration):
                    scanners[index].beacons.append(
                        beacon.rotate_x(perm[0]).rotate_y(perm[1]).rotate_z(perm[2])
                    )
                    index += 1

        # remove duplicates
        to_return = [scanners[0]]
        for scanner in scanners:
            duplicate = False
            for check in to_return:
                if scanner == check:
                    duplicate = True
            if not duplicate:
                to_return.append(scanner)

        return to_return

    def to_absolute(self):
        if self.abs_coord is not None:
            for i in range(len(self.beacons)):
                self.beacons[i] = self.beacons[i].translate(self.abs_coord[0], self.abs_coord[1], self.abs_coord[2])

    def __eq__(self, other):
        for i, beacon1 in enumerate(self.beacons):
            if beacon1 != other.beacons[i]:
                return False
        return True

    def __repr__(self):
        string = f"--- scanner {self.id} ---\n"
        for beacon in self.beacons:
            string += str(beacon.x) + ',' + str(beacon.y) + ',' + str(beacon.z) + '\n'
        return string


class Beacon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotate_x(self, times):
        angle = radians(times * 90)
        new_x = self.x
        new_y = round(self.y * cos(angle) - self.z * sin(angle))
        new_z = round(self.y * sin(angle) + self.z * cos(angle))
        return Beacon(new_x, new_y, new_z)

    def rotate_y(self, times):
        angle = radians(times * 90)
        new_x = round(self.x * cos(angle) + self.z * sin(angle))
        new_y = self.y
        new_z = round(- self.x * sin(angle) + self.z * cos(angle))
        return Beacon(new_x, new_y, new_z)

    def rotate_z(self, times):
        angle = radians(times * 90)
        new_x = round(self.x * cos(angle) - self.y * sin(angle))
        new_y = round(self.x * sin(angle) + self.y * cos(angle))
        new_z = self.z
        return Beacon(new_x, new_y, new_z)

    def translate(self, x, y, z):
        return Beacon(self.x + x, self.y + y, self.z + z)

    def __sub__(self, other):
        return Beacon(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neg__(self):
        return Beacon(-self.x, -self.y, -self.z)

    def __repr__(self):
        return str(self.x) + ',' + str(self.y) + ',' + str(self.z)


def read_input():
    scanners = []
    with open("input19.txt") as f:
        cur_scanner = None
        for line in f:
            if line.startswith('---'):
                split = line.split()
                cur_scanner = Scanner(int(split[2]))
            elif line == '\n':
                scanners.append(cur_scanner)
            else:
                split = line.split(',')
                cur_scanner.beacons.append(Beacon(int(split[0]), int(split[1]), int(split[2])))
    scanners[0].abs_coord = (0, 0, 0)
    return scanners


def compare_beacons(scanner1, scanner2):
    # check if 12 beacons overlap
    for beacon1 in scanner1.beacons:
        for beacon2 in scanner2.beacons:
            # try beacon1 == beacon2
            # translation = beacon2 - beacon1
            # translate every other point in beacon2 and check how many points overlap
            translation = -(beacon2 - beacon1)
            trans_beacons = [beacon.translate(translation.x, translation.y, translation.z) for beacon in
                             scanner2.beacons]
            overlaps = 0
            for coord1 in scanner1.beacons:
                for coord2 in trans_beacons:
                    if coord1 == coord2:
                        overlaps += 1

            if overlaps >= 12:
                return translation
    return None


def find_absolute_mapping(scanner, abs_mappings):
    for abs_scanner in abs_mappings:
        for oriented_scanner in scanner.all_orientations():
            abs_coord = compare_beacons(abs_scanner, oriented_scanner)
            if abs_coord is not None:
                oriented_scanner.abs_coord = (abs_coord.x, abs_coord.y, abs_coord.z)
                oriented_scanner.to_absolute()
                return oriented_scanner


def map_scanners(scanners):
    counter = 0
    found = [scanners[0]]
    to_find = scanners[1:]
    found_last_it = [scanners[0]]
    while to_find:
        cur_it = []
        print(counter)
        for scanner in to_find:
            if not found_last_it:
                found_last_it = found
            mapping = find_absolute_mapping(scanner, found_last_it)
            if mapping is not None:
                found.append(mapping)
                cur_it.append(mapping)
                to_find.remove(scanner)
                counter += 1
        found_last_it = cur_it
    return found


def all_beacons(scanners):
    beacons = []
    for scanner in scanners:
        beacons += scanner.beacons

    to_return = []
    for beacon in beacons:
        duplicate = False
        for check in to_return:
            if beacon == check:
                duplicate = True
                break
        if not duplicate:
            to_return.append(beacon)

    return to_return


def manhattan_distance(scanner1, scanner2):
    return abs(scanner1.abs_coord[0] - scanner2.abs_coord[0]) + abs(
        scanner1.abs_coord[1] - scanner2.abs_coord[1]) + abs(scanner1.abs_coord[2] - scanner2.abs_coord[2])


def part1():
    scanners = read_input()
    abs_scanners = map_scanners(scanners)
    beacons = all_beacons(abs_scanners)
    return len(beacons)


def part2():
    scanners = read_input()
    abs_scanners = map_scanners(scanners)
    distances = []
    for scanner1 in abs_scanners:
        for scanner2 in abs_scanners:
            distance = manhattan_distance(scanner1, scanner2)
            distances.append(distance)
    return max(distances)


print(part2())
