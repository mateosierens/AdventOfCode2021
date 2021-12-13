class Node:
    def __init__(self, name: str, big_cave: bool):
        self.name = name
        self.big_cave = big_cave
        self.neighbours = []


def read_input():
    graph = []
    node_dict = {}
    with open("input12.txt") as f:
        for line in f:
            transition = line[:-1].split('-')
            for node in transition:
                if node not in node_dict:
                    big = node[0].isupper()
                    new_node = Node(node, big)
                    node_dict[node] = new_node
                    graph.append(new_node)
            node1 = node_dict[transition[0]]
            node2 = node_dict[transition[1]]
            node1.neighbours.append(node2)
            node2.neighbours.append(node1)
    return graph


def recursive_visit(graph, current_node, current_path, paths):
    if current_node.name == "end":
        paths.append(current_path)
    else:
        for node in current_node.neighbours:
            if node.big_cave or (not node.big_cave and node.name not in current_path):
                new_path = current_path + [node.name]
                recursive_visit(graph, node, new_path, paths)
    return paths


def recursive_visit_advanced(graph, current_node, current_path, paths, double_small):
    if current_node.name == "end":
        paths.append(current_path)
    else:
        for node in current_node.neighbours:

            if node.big_cave or (not node.big_cave and node.name not in current_path):
                new_path = current_path + [node.name]
                recursive_visit_advanced(graph, node, new_path, paths, double_small)
            elif not double_small and node.name != "start":
                new_path = current_path + [node.name]
                recursive_visit_advanced(graph, node, new_path, paths, True)
    return paths


def part1():
    graph = read_input()
    start = next(node for node in graph if node.name == "start")
    paths = recursive_visit(graph, start, ["start"], [])
    return len(paths)

def part2():
    graph = read_input()
    start = next(node for node in graph if node.name == "start")
    paths = recursive_visit_advanced(graph, start, ["start"], [], False)
    return len(paths)

print(part2())
