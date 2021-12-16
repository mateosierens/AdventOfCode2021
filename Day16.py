import operator


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []


def read_input():
    scale = 16
    with open("input16.txt") as f:
        hex = f.readline()[:-1]
        binary_string = bin(int(hex, scale))[2:].zfill(len(hex) * 4)
        return binary_string


def read_literal(binary):
    # literal value
    counter = 0
    last_segment = False
    literal = ""
    while not last_segment:
        literal += binary[counter + 1:counter + 5]
        if binary[counter] == '0':
            last_segment = True
        counter += 5
    return int(literal, 2), counter


def get_length(subpacket):
    type_ID = int(subpacket[3:6], 2)
    if type_ID == 4:
        return read_literal(subpacket[6:])[1] + 6
    else:
        length_type_ID = int(subpacket[6])
        if length_type_ID:
            # we know number of subpackets, find length of these subpackets
            length = 6 + 11 + 1
            subpackets = int(subpacket[7:18], 2)
            packet_start = 18
            for _ in range(subpackets):
                sub_length = get_length(subpacket[packet_start:])
                packet_start += sub_length
                length += sub_length
            return length
        else:
            # next 15 bits represent total length in bits of the subpackets
            return int(subpacket[7:22], 2) + 6 + 1 + 15


operation_dict = {0: operator.add, 1: operator.mul, 2: min, 3: max, 5: operator.gt, 6: operator.lt, 7: operator.eq}


def read_packet(binary):
    # make substrings
    version = int(binary[0:3], 2)
    type_ID = int(binary[3:6], 2)

    # if literal
    if type_ID == 4:
        literal = read_literal(binary[6:])
        return version, Node(literal[0])

    else:
        # operator, read subpackets
        node = Node(operation_dict[type_ID])
        length_type_ID = int(binary[6])
        if length_type_ID:
            # next 11 bits represent number of sub-packets
            subpackets = int(binary[7:18], 2)
            packet_start = 18
            version_sum = version
            for _ in range(subpackets):
                packet_end = packet_start + get_length(binary[packet_start:])
                new_versions, new_node = read_packet(binary[packet_start:packet_end])
                node.children.append(new_node)
                version_sum += new_versions
                packet_start = packet_end
            return version_sum, node
        else:
            # next 15 bits represent total length in bits of the subpackets
            sub_length = int(binary[7:22], 2)
            packet_start = 22
            version_sum = version
            while packet_start < 22 + sub_length:
                packet_end = packet_start + get_length(binary[packet_start:])
                new_versions, new_node = read_packet(binary[packet_start:packet_end])
                node.children.append(new_node)
                version_sum += new_versions
                packet_start = packet_end
            return version_sum, node


def part1():
    return read_packet(read_input())[0]


def compute(node):
    if not node.children:
        return node.value
    else:
        if len(node.children) == 2:
            return int(node.value(compute(node.children[0]), compute(node.children[1])))
        else:
            total = compute(node.children[0])
            for child in node.children[1:]:
                total = node.value(total, compute(child))
            return total


def part2():
    versions, operation_tree = read_packet(read_input())
    return compute(operation_tree)


print(part2())
