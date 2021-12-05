def read_input():
    number_order = []
    bingo_boards = []
    with open("input4.txt") as f:
        first = True
        new_board = []
        for line in f:
            if first:
                number_order = [int(number) for number in line.split(',')]
                first = False
            else:
                # when encountering a new line, next 5 lines are a board
                if line == "\n":
                    if new_board:  # only append if board isnt empty
                        bingo_boards.append(new_board)
                    new_board = []
                else:
                    # keep tuple per number, boolean value represents marking
                    row = [[int(number), False] for number in line.split()]
                    new_board.append(row)
    return number_order, bingo_boards

def mark_number(number, boards):
    for board in boards:
        for row in board:
            for entry in row:
                if entry[0] == number:
                    entry[1] = True
    return boards

def check_board(board):
    # check rows
    for row in board:
        win = True
        for entry in row:
            if not entry[1]:
                win = False
                break
        if win:
            return True

    # check columns
    for col in range(len(board)):
        win = True
        for row in range(len(board)):
            if not board[row][col][1]:
                win = False
                break
        if win:
            return True

    return False

def get_unmarked_numbers(board):
    to_return = []
    for row in board:
        for entry in row:
            if not entry[1]:
                to_return.append(entry[0])
    return to_return

def part1():
    numbers, boards = read_input()
    for number in numbers:
        boards = mark_number(number, boards)
        for board in boards:
            if check_board(board):
                total = sum(get_unmarked_numbers(board))
                score = total * number
                return score
    return -1

def part2():
    numbers, boards = read_input()
    for number in numbers:
        boards = mark_number(number, boards)
        new_boards = []
        for board in boards:
            if check_board(board) and len(boards) > 1:
                pass
            elif check_board(board) and len(boards) == 1:
                total = sum(get_unmarked_numbers(board))
                score = total * number
                return score
            else:
                new_boards.append(board)
        boards = new_boards
    return -1

print(part2())