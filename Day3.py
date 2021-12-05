def bytestringToInt(byte):
    result = 0
    for i, bit in enumerate(byte):
        result += int(byte[i]) * 2 ** (len(byte) - 1 - i)
    return result

def occurences(byte_list, pos):
    """
    Given a list of bytes, determine what bit occurs most and least at given position
    :param byte_list: List of bytes to check
    :param pos: Position to check in each byte
    :return: tuple of most occuring and least occuring bit
    """
    occurence = {'0': 0, '1': 0}
    for byte in byte_list:
        occurence[byte[pos]] += 1
    if occurence['0'] > occurence['1']:
        return 0, 1
    elif occurence['1'] > occurence['0']:
        return 1, 0
    else:
        # states both occur equally
        return 1, 0

def getBytes(byte_list, pos, bit):
    """
    Get all bytes that have a given bit on a given position
    :param byte_list: List of all bytes to check
    :param pos: Position in the byte to check
    :param bit: The bit that is required at given position
    :return: A list of bytes that satisfy the requirements
    """
    return [byte for byte in byte_list if int(byte[pos]) == bit]

def part1():
    with open("input3.txt") as f:
        bit_dict = dict()
        bytelength = 0
        for line in f:
            bytestream = line[:-1]
            bytelength = len(bytestream)
            for position in range(bytelength):
                # entry in dict based on position and bit
                key = str(position) + bytestream[position]
                bit_dict[key] = 0 if key not in bit_dict else bit_dict[key] + 1

        gamma = ""
        epsilon = ""
        for i in range(bytelength):
            if bit_dict[str(i) + "0"] > bit_dict[str(i) + "1"]:
                gamma += "0"
                epsilon += "1"
            else:
                gamma += "1"
                epsilon += "0"
        power = bytestringToInt(gamma) * bytestringToInt(epsilon)
        print(power)

def part2():
    with open("input3.txt") as f:
        byte_list = []
        for line in f:
            byte_list.append(line[:-1])

        oxygen_candidates = byte_list
        i = 0
        while len(oxygen_candidates) > 1:
            best_bit = occurences(oxygen_candidates, i)[0]
            oxygen_candidates = getBytes(oxygen_candidates, i, best_bit)
            i += 1
        co2_candidates = byte_list
        i = 0
        while len(co2_candidates) > 1:
            best_bit = occurences(co2_candidates, i)[1]
            co2_candidates = getBytes(co2_candidates, i, best_bit)
            i += 1
        life_support = bytestringToInt(oxygen_candidates[0]) * bytestringToInt(co2_candidates[0])
        print(life_support)

part2()