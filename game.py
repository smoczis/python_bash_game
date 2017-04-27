import os
import sys
import tty
import termios
from maps_functions import *

COLOURS = {'X': '\x1b[0;31;41m'+'X'+'\x1b[0m', 'G': '\x1b[0;32;42m'+'G'+'\x1b[0m', 'N': '\x1b[0;34;44m'+'N'+'\x1b[0m'}
BLOCKERS = [COLOURS['X'], COLOURS['G'], COLOURS['N']]


def create_board(width, height):
    width = int(width)
    height = int(height)
    board = []
    for line in range(1, height + 1):
        if line in [1, height]:
            board.append(["X" for column in range(1, width+1)])
        else:
            board.append(["X"] + [" " for column in range(2, width)] + ["X"])
    return board


def print_board(board):
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=107))
    os.system('clear')
    for line in board:
        print("".join(line))


def insert_player(board, x, y):
    board[y][x] = "@"
    return board


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch.lower()


def move(board, x, y):
    global BLOCKERS
    key = getch()
    board[y][x] = " "
    if key == "a" and board[y][x-1] not in BLOCKERS:
        x -= 1
    elif key == "d" and board[y][x+1] not in BLOCKERS:
        x += 1
    elif key == "w" and board[y-1][x] not in BLOCKERS:
        y -= 1
    elif key == "s" and board[y+1][x] not in BLOCKERS:
        y += 1
    elif key == "m":
        sys.exit()
    else:
        pass
    return x, y


def main():
    wall = ['X', 'G', 'N', 'B']
    height, width = 39, 100
    board = import_map('map1.txt')
    pos = 36, 13
    print('\x1b[3;31;41m'+'X'+'\x1b[0m')
    insert_player(board, pos[0], pos[1])
    print_board(board)
    while True:
        pos = move(board, pos[0], pos[1])
        insert_player(board, pos[0], pos[1])
        print_board(board)


if __name__ == '__main__':
    main()
