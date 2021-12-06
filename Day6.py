def read_input():
    with open("input6.txt") as f:
        line = f.readline()
        return [int(age) for age in line.split(',')]

def cycle_age(age_list):
    new_fish = []
    new_age_list = []
    for age in age_list:
        age -= 1
        if age < 0:
            new_age_list.append(6)
            new_fish.append(8)
        else:
            new_age_list.append(age)
    return new_age_list + new_fish

def part1():
    fish = read_input()
    for i in range(80):
        fish = cycle_age(fish)
    print(len(fish))

def synced_fish_dict(age_list):
    """
    Create a dict of the fish that are in sync, key is the counter, value is the amount of fish with this counter
    """
    synced_fish = dict()
    for i in range(7):
        count = age_list.count(i)
        synced_fish[i] = count
    return synced_fish

def cycle_age_dict(synced_fish):
    new_dict = dict()
    for key, value in synced_fish.items():
        counter = key - 1
        if counter < 0:
            if 6 not in new_dict:
                new_dict[6] = value
            else:
                new_dict[6] += value
            new_dict[8] = value
        else:
            if counter not in new_dict:
                new_dict[counter] = value
            else:
                new_dict[counter] += value
    return new_dict

def part2():
    fish = read_input()
    synced_fish = synced_fish_dict(fish)
    for i in range(256):
        synced_fish = cycle_age_dict(synced_fish)
    print(sum([value for key, value in synced_fish.items()]))

part2()