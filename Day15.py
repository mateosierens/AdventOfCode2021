from math import inf
from queue import PriorityQueue
from copy import deepcopy

class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.dijkstra_value = inf
        self.parent = None

    def __repr__(self):
        return str(self.value)

    def __lt__(self, other):
        return self.dijkstra_value < other.dijkstra_value

def read_input():
    grid = []
    with open("input15.txt") as f:
        for y, line in enumerate(f):
            row = []
            for x, char in enumerate(line[:-1]):
                row.append(Node(x, y, int(char)))
            grid.append(row)
    return grid

def get_neighbours(x, y, grid):
    neighbours = []
    length = len(grid)
    for i in [-1, 1]:
        new_x = x + i
        new_y = y + i
        if 0 <= new_x < length:
            new_neighbour = grid[y][new_x]
            neighbours.append(new_neighbour)
        if 0 <= new_y < length:
            new_neighbour = grid[new_y][x]
            neighbours.append(new_neighbour)
    return neighbours

def relax(node, neighbour):
    if neighbour.dijkstra_value > node.dijkstra_value + neighbour.value:
        neighbour.dijkstra_value = node.dijkstra_value + neighbour.value
        neighbour.parent = node
        return True
    return False

def shortest_path(grid):
    start = grid[0][0]
    start.dijkstra_value = 0
    S = []
    Q = PriorityQueue()
    Q.put(start)
    while not Q.empty():
        current_node = Q.get()
        S.append(current_node)
        neighbours = get_neighbours(current_node.x, current_node.y, grid)
        for neighbour in neighbours:
            if relax(current_node, neighbour):
                Q.put(neighbour)
    return grid[len(grid) - 1][len(grid) - 1].dijkstra_value

def expand_grid(grid):
    # create 9 different tiles from original grid
    grids = []
    for i in range(9):
        new_grid = []
        for row in grid:
            new_row = []
            for node in row:
                value = node.value + i if node.value + i <= 9 else (node.value + i) % 9
                new_row.append(Node(node.x, node.y, value))
            new_grid.append(new_row)
        grids.append(new_grid)

    # create one big grid from created grids
    big_grid = []
    for i in range(5):
        new_tiles_row = [[] for _ in range(len(grid))]
        for j in range(5):
            for row in range(len(grid)):
                new_tiles_row[row] += deepcopy(grids[i + j][row])
        for tiles_row in new_tiles_row:
            big_grid.append(tiles_row)

    # update coords
    for y, row in enumerate(big_grid):
        for x, node in enumerate(row):
            node.x, node.y = x, y

    return big_grid

def part1():
    grid = read_input()
    shortest = shortest_path(grid)
    return shortest

def part2():
    grid = read_input()
    big_grid = expand_grid(grid)
    shortest = shortest_path(big_grid)
    return shortest

print(part2())