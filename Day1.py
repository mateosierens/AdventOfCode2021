def part1():
    with open("input1.txt") as f:
        last_depth = -1
        counter = 0
        for line in f:
            depth = int(line[:-1])
            if last_depth != -1 and depth > last_depth:
                counter += 1
            last_depth = depth
        print(counter)

def part2():
    with open("input1.txt") as f:
        last_depth = -1
        counter = 0
        windows = []
        for line in f:
            depth = int(line[:-1])
            windows.append([depth])
            for window in windows:
                if window != windows[-1]:
                    window.append(depth)
            if len(windows[0]) < 3:
                continue
            depth_sum = sum(windows[0])
            if last_depth != -1 and depth_sum > last_depth:
                counter += 1
            last_depth = depth_sum
            windows.pop(0)
        print(counter)

part2()
