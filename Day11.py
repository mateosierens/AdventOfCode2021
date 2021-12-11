def read_input():
    octopuses = []
    with open("input11.txt") as f:
        for line in f:
            octopuses.append([int(char) for char in line[:-1]])
    return octopuses

def increase_energy(octopuses):
    to_flash = []  # make queue of octopuses that have to flash
    for x in range(len(octopuses)):
        for y in range(len(octopuses)):
            octopuses[x][y] += 1
            if octopuses[x][y] > 9:
                to_flash.append((x, y))
    return octopuses, to_flash

def get_neighbours(x, y, length):
    neighbours = []
    for i in [-1 , 1]:
        for j, k in [(x + i, y), (x, y + i), (x + i, y + i), (x + i, y - i)]:
            if 0 <= j < length and 0 <= k < length:
                neighbours.append((j, k))
    return neighbours

def recursive_flashes(octopuses, to_flash):
    while to_flash:
        new_flashes = []
        for oct_coord in to_flash:
            neighbours = get_neighbours(oct_coord[0], oct_coord[1], len(octopuses))
            for x, y in neighbours:
                if octopuses[x][y] <= 9:
                    octopuses[x][y] += 1
                    if octopuses[x][y] > 9:
                        new_flashes.append((x, y))
        to_flash = new_flashes

    # return flashed octopuses energy to zero
    flash_count = 0
    for x in range(len(octopuses)):
        for y in range(len(octopuses)):
            if octopuses[x][y] > 9:
                octopuses[x][y] = 0
                flash_count += 1
    return octopuses, flash_count

def zero_grid(octopuses):
    for row in octopuses:
        for octopus in row:
            if octopus != 0:
                return False
    return True

def part1():
    octopuses = read_input()
    flash_count = 0
    for _ in range(100):
        octopuses, to_flash = increase_energy(octopuses)
        octopuses, new_flashes = recursive_flashes(octopuses, to_flash)
        flash_count += new_flashes
    return flash_count

def part2():
    octopuses = read_input()
    step_count = 0
    while not zero_grid(octopuses):
        octopuses, to_flash = increase_energy(octopuses)
        octopuses, new_flashes = recursive_flashes(octopuses, to_flash)
        step_count += 1
    return step_count

print(part2())