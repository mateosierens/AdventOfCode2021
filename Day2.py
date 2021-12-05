def part1():
    with open("input2.txt") as f:
        h_pos = 0
        d_pos = 0
        for line in f:
            split = line.split()
            move = split[0]
            amount = int(split[1])
            if move == "forward":
                h_pos += amount
            elif move == "down":
                d_pos += amount
            elif move == "up":
                d_pos -= amount
        print(h_pos * d_pos)

def part2():
    with open("input2.txt") as f:
        h_pos = 0
        d_pos = 0
        aim = 0
        for line in f:
            split = line.split()
            move = split[0]
            amount = int(split[1])
            if move == "forward":
                h_pos += amount
                d_pos += amount * aim
            elif move == "down":
                aim += amount
            elif move == "up":
                aim -= amount
        print(h_pos * d_pos)

part2()