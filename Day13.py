def read_input():
    dots = []
    fold_sequence = []
    reading_dots = True
    with open("input13.txt") as f:
        for line in f:
            if line == '\n':
                reading_dots = False
                continue
            if reading_dots:
                coords = [int(coord) for coord in line[:-1].split(',')]
                dots.append((coords[0], coords[1]))
            else:
                fold = line[:-1].split()[2]
                fold_sequence.append(fold)
    return dots, fold_sequence


def fold(coords, instruction):
    new_coords = []
    axis = instruction[0]
    fold_line = int(instruction[2:])
    for coord in coords:
        if axis == 'x':
            if coord[0] < fold_line:
                new_coords.append(coord)
            else:
                new_x = fold_line - (coord[0] - fold_line)
                new_coords.append((new_x, coord[1]))
        else:
            if coord[1] < fold_line:
                new_coords.append(coord)
            else:
                new_y = fold_line - (coord[1] - fold_line)
                new_coords.append((coord[0], new_y))
    return list(set(new_coords))


def print_dots(dots):
    string = ""
    sorted_dots = sorted(dots, key=lambda coord: coord[1])
    biggest_y = sorted_dots[-1][1]
    biggest_x = max([coord[0] for coord in dots])
    for y in range(biggest_y + 1):
        row = [coord for coord in dots if coord[1] == y]
        for x in range(biggest_x + 1):
            if (x, y) in row:
                string += '#'
            else:
                string += '.'
        string += '\n'
    print(string)

def part1():
    dots, fold_sequence = read_input()
    new_dots = fold(dots, fold_sequence[0])
    return len(new_dots)


def part2():
    dots, fold_sequence = read_input()
    for fold_instruction in fold_sequence:
        dots = fold(dots, fold_instruction)
    print_dots(dots)

part2()
