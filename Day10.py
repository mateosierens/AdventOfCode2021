def read_input():
    lines = []
    with open("input10.txt") as f:
        for line in f:
            lines.append(line[:-1])
    return lines

def check_corruptness(line):
    bracket_stack = []
    # keep a dict that translates closing brackets to opening brackets
    bracket_translator = {')': '(', ']': '[', '}': '{', '>': '<'}
    bracket_points = {')': 3, ']': 57, '}': 1197, '>': 25137}
    for char in line:
        if char in [')', ']', '}', '>']:
            opening_bracket = bracket_translator[char]
            bracket = bracket_stack.pop()
            if bracket != opening_bracket:
                return bracket_points[char]
        else:
            bracket_stack.append(char)
    return 0

def check_incomplete(line):
    bracket_stack = []
    # keep a dict that translates opening brackets to closing brackets
    bracket_translator = {'(': ')', '[': ']', '{': '}', '<': '>'}
    bracket_points = {')': 1, ']': 2, '}': 3, '>': 4}
    for char in line:
        if char in [')', ']', '}', '>']:
            bracket_stack.pop()
        else:
            bracket_stack.append(char)

    # now get missing brackets
    score = 0
    while bracket_stack:
        opening_bracket = bracket_stack.pop()
        closing_bracket = bracket_translator[opening_bracket]
        score *= 5
        score += bracket_points[closing_bracket]
    return score

def part1():
    lines = read_input()
    score = 0
    for line in lines:
        score += check_corruptness(line)
    return score

def part2():
    lines = read_input()
    scores = []
    for line in lines:
        if check_corruptness(line) == 0:
            scores.append(check_incomplete(line))
    scores.sort()
    mid = (len(scores) + 1) // 2
    score = scores[mid - 1]
    return score

print(part2())