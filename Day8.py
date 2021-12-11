def read_input():
    inputs = []
    outputs = []
    with open("input8.txt") as f:
        for line in f:
            split = line.split('|')
            inputs.append(split[0].split())
            outputs.append(split[1].split())
    return inputs, outputs

"""
 0000
1    2
1    2
 3333
4    5
4    5
 6666
"""

digit_segments = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}
digit_map = {0: [0, 1, 2, 4, 5, 6],
             1: [2, 5],
             2: [0, 2, 3, 4, 6],
             3: [0, 2, 3, 5, 6],
             4: [1, 2, 3, 5],
             5: [0, 1, 3, 5, 6],
             6: [0, 1, 3, 4, 5, 6],
             7: [0, 2, 5],
             8: [0, 1, 2, 3, 4, 5, 6],
             9: [0, 1, 2, 3, 5, 6]}
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

def part1():
    _, outputs = read_input()
    total = 0
    to_check = [1, 4, 7, 8]
    for output in outputs:
        for digit in to_check:
            total += sum([1 for entry in output if len(entry) == digit_segments[digit]])
    return total

def get_unique_inputs(input):
    # return the inputs for numbers 1, 4, 7, 8
    number_input = dict()
    to_check = [1, 4, 7, 8]
    for number in to_check:
        for entry in input:
            if len(entry) == digit_segments[number]:
                number_input[number] = entry
                break
    return number_input

def check_intersections_complements(number_string, mapping):
    new_mapping = True
    while new_mapping:
        new_mapping = False
        for number1, string1 in number_string.items():
            for number2, string2 in number_string.items():
                if number1 != number2:
                    segments1 = digit_map[number1]
                    segments2 = digit_map[number2]

                    # check intersection
                    intersection = list(set(segments1).intersection(segments2))
                    intersection = [entry for entry in intersection if entry not in mapping]
                    if len(intersection) == 1 and intersection[0] not in mapping:
                        new_mapping = True
                        new_letter = list(set(string1).intersection(string2))
                        new_letter = [letter for letter in new_letter if letter not in mapping.values()]
                        mapping[intersection[0]] = new_letter[0]

                    # check complement
                    if len(segments1) < len(segments2):
                        segments1, segments2 = segments2, segments1
                        string1, string2 = string2, string1
                        number1, number2 = number2, number1
                    complement = [entry for entry in segments1 if entry not in segments2]
                    complement = [entry for entry in complement if entry not in mapping]
                    if len(complement) == 1 and complement[0] not in mapping:
                        new_mapping = True
                        new_letter = [char for char in string1 if char not in string2]
                        new_letter = [letter for letter in new_letter if letter not in mapping.values()]
                        mapping[complement[0]] = new_letter[0]
    return mapping

def find_string_candidate(number, number_string, mapping, strings):
    # first, find all strings that match the number based on the current known mapping of segments
    segments = digit_map[number]
    candidates = [_ for _ in strings]
    for segment in segments:
        if segment in mapping:
            for string in strings:
                if mapping[segment] not in string or len(string) != len(segments) or string in number_string.values():
                    candidates.remove(string)

    # now check if candidates can be trimmed down, preferably to one
    # do this by checking the strings that numbers are known for, and comparing
    for compare_number, compare_string in number_string.items():
        # check by how many segments intersect, how many letters in the string should be the same
        compare_segments = digit_map[compare_number]
        amount = len(set(segments).intersection(compare_segments))

        # loop over candidates and remove candidates that do not satisfy the string intersection
        remaining_candidates = []
        for candidate in candidates:
            if len(set(candidate).intersection(compare_string)) == amount:
                remaining_candidates.append(candidate)
        candidates = remaining_candidates
    return candidates

def create_mapping(string_input):
    # create a mapping to determine which segment of the digital number is represented by which letter
    # to do this, knowing which input represent which number helps us
    number_string = get_unique_inputs(string_input)
    mapping = dict()
    while len(mapping) != 7:
        # determine which segment represent which number by taking the intersections and complement of the known numbers
        mapping = check_intersections_complements(number_string, mapping)

        # based on new mapping and known string, find string for unknown numbers
        for number in range(10):
            if number not in number_string:
                candidates = find_string_candidate(number, number_string, mapping, string_input)
                if len(candidates) == 1:
                    number_string[number] = candidates[0]

    return number_string, mapping


def translate_number(strings, number_string):
    digits = ""
    for input in strings:
        for number, string in number_string.items():
            if sorted(input) == sorted(string):
                digits += str(number)
                break

    return int(digits)


def part2():
    inputs, outputs = read_input()
    total = 0
    for i, input in enumerate(inputs):
        number_string, mapping = create_mapping(input)
        total += translate_number(outputs[i], number_string)
    return total

print(part2())

