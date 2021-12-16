def read_input():
    initial_string = ""
    rules = {}
    with open("input14.txt") as f:
        for i, line in enumerate(f):
            if i == 0:
                initial_string = line[:-1]
            elif i > 1:
                split = line[:-1].split()
                rules[split[0]] = split[2]
    return initial_string, rules

def string_to_occurences(string):
    occurences = {}
    for i in range(len(string) - 1):
        pair = string[i] + string[i + 1]
        if pair not in occurences:
            occurences[pair] = 1
        else:
            occurences[pair] += 1
    return occurences

def iteration(occurences, rules):
    new_occurences = {}
    for key, value in occurences.items():
        new_pair1, new_pair2 = key[0] + rules[key], rules[key] + key[1]
        new_occurences[new_pair1] = value if new_pair1 not in new_occurences else new_occurences[new_pair1] + value
        new_occurences[new_pair2] = value if new_pair2 not in new_occurences else new_occurences[new_pair2] + value
    return new_occurences

def count_occurences(occurences, initial_string):
    char_occurences = {}
    for key, value in occurences.items():
        char = key[0]
        char_occurences[char] = value if char not in char_occurences else char_occurences[char] + value
    last_char = initial_string[-1]
    char_occurences[last_char] += 1
    return char_occurences

def part1():
    init_string, rules = read_input()
    occurences = string_to_occurences(init_string)
    for _ in range(10):
        occurences = iteration(occurences, rules)
    char_occurences = count_occurences(occurences, init_string)
    return max(char_occurences.values()) - min(char_occurences.values())

def part2():
    init_string, rules = read_input()
    occurences = string_to_occurences(init_string)
    for _ in range(40):
        occurences = iteration(occurences, rules)
    char_occurences = count_occurences(occurences, init_string)
    return max(char_occurences.values()) - min(char_occurences.values())

print(part2())