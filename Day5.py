def read_input():
    lines = []  # list of tuples of lines, that are also stored as tuples
    with open("input5.txt") as f:
        for line in f:
            split = line.split()
            line_begin = (int(split[0].split(',')[0]), int(split[0].split(',')[1]))
            line_end = (int(split[2].split(',')[0]), int(split[2].split(',')[1]))
            lines.append((line_begin, line_end))
    return lines


def create_grid(lines, diagonals=False):
    # grid is 999 x 999
    grid = [[0 for i in range(999)] for j in range(999)]
    for line in lines:
        x1, y1 = line[0][0], line[0][1]
        x2, y2 = line[1][0], line[1][1]

        # straight lines
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            for i in range(y1, y2 + 1):
                grid[x1][i] += 1
        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            for i in range(x1, x2 + 1):
                grid[i][y1] += 1

        # if diagonals have to be taken into account
        elif diagonals:
            mirror_x = 0
            mirror_y = 0

            # if var1 is bigger than var2 mirror the coordinate to reduce loops and conditions
            if x1 > x2:
                mirror_x = 2 * (x1 - x2)
            if y1 > y2:
                mirror_y = 2 * (y1 - y2)
            counter = 0
            for i, j in zip(range(x1, x2 + 1 + mirror_x), range(y1, y2 + 1 + mirror_y)):
                row = i
                col = j
                if mirror_x:
                    row -= 2 * counter
                if mirror_y:
                    col -= 2 * counter
                grid[row][col] += 1
                counter += 1

    return grid


def part1():
    grid = create_grid(read_input())
    counter = 0
    for row in grid:
        for pos in row:
            if pos > 1:
                counter += 1
    print(counter)


def part2():
    grid = create_grid(read_input(), diagonals=True)
    counter = 0
    for row in grid:
        for pos in row:
            if pos > 1:
                counter += 1
    print(counter)


part2()
