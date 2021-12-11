def read_input():
    heightmap = []
    with open("input9.txt") as f:
        for line in f:
            line = line[:-1]
            heightmap.append([int(char) for char in line])
    return heightmap

def get_neighbours(x, y, length):
    neighbours = []
    for i in [-1 , 1]:
        new_x = x + i
        new_y = y + i
        if new_x >= 0 and new_x < length:
            neighbours.append((new_x, y))
        if new_y >= 0 and new_y < length:
            neighbours.append((x, new_y))
    return neighbours

def is_lowpoint(x, y, heightmap):
    lowpoint = True
    value = heightmap[x][y]
    for neighbour in get_neighbours(x, y, len(heightmap)):
        if heightmap[neighbour[0]][neighbour[1]] <= value:
            lowpoint = False
            break
    return lowpoint

def find_basins(heightmap):
    basins = []
    checked = []
    length = len(heightmap)
    for x in range(length):
        for y in range(length):
            if (x, y) not in checked and heightmap[x][y] != 9:
                new_basin = [(x, y)]
                to_check = [(x, y)]
                while to_check:
                    new_points = []
                    for point in to_check:
                        neighbours = get_neighbours(point[0], point[1], length)
                        for neighbour in neighbours:
                            neighbour_value = heightmap[neighbour[0]][neighbour[1]]
                            if neighbour_value != 9 and neighbour not in new_basin:
                                new_basin.append(neighbour)
                                new_points.append(neighbour)
                    for point in new_points:
                        to_check.append(point)
                    checked_point = to_check.pop(0)
                    checked.append(checked_point)
                basins.append(new_basin)
    return basins

def part1():
    risk_levels = []
    heightmap = read_input()
    for x, row in enumerate(heightmap):
        for y, point in enumerate(row):
            if is_lowpoint(x, y, heightmap):
                risk_levels.append(1 + point)
    return sum(risk_levels)

def part2():
    heightmap = read_input()
    basins = find_basins(heightmap)
    basin_sizes = [len(i) for i in basins]
    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]

print(part2())