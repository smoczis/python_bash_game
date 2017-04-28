import os
import sys
import tty
import termios
import random
import time
from re import match
from maps_creator import *
from hero import *


COLOURS = {'X': '\x1b[0;31;41m'+'X'+'\x1b[0m', 'G': '\x1b[0;32;42m'+'G'+'\x1b[0m', 'N': '\x1b[0;34;44m'+'N'+'\x1b[0m'}
BLOCKERS = [COLOURS['X'], COLOURS['G'], COLOURS['N']]

HINTS = {
        '0': [("Type the capital of Poland", "Warsaw"), ("Type the capital of France", "Paris"),
              ("Dupa cycki lasery", "Dzoana Krupa")],
        '1': ['Type the factorial of number 3', '6'],
        '2': ['What the \'int\' abbreviate for?', 'integer']
}


def hide_mines(actual):
    """hiding all mines, that were printed before by show_neighbours()"""
    for line_i in range(len(actual.board)):
        for char_i in range(len(actual.board[line_i])):
            if actual.board[line_i][char_i] == 'X':
                actual.board[line_i][char_i] = ' '
    return actual.board


def calc_neighbours(actual, x, y, distance=1):
    """calculating and set to list all board cells in given distance (default 1) from x, y"""
    neighbours = []
    for delta_y in range(-distance, distance + 1):
        for delta_x in range(-distance, distance + 1):
            if y + delta_y in range(len(actual.board)) and x + delta_x in range(len(actual.board[0])):
                neighbours.append((x + delta_x, y + delta_y))
    return neighbours


def show_neighbours(actual, neighbours):
    """showing on board all hidden objects in distance
       (calculated by calc_neighbours) of player's position. return board"""
    for (x, y) in neighbours:
        if (x, y) in actual.mines:
            actual.board[y][x] = "X"
    return actual.board


def insert_player(actual, x, y, detector=False):
    """inserting player on board on given position. in future, it may get players atributes, to diverse result"""
    global COLOURS
    if detector:
        see_distance = 5
    else:
        see_distance = 1
    hide_mines(actual)
    neighbours = calc_neighbours(actual, x, y, see_distance)
    show_neighbours(actual, neighbours)
    actual.board[y][x] = "@"
    return actual.board


def getch():
    """read users input without pressing 'return'. returns one (first) char of input"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch.lower()


def react(actual, x, y):
    for mine in actual.mines:
        if mine in calc_neighbours(actual, x, y):
            actual.mines.remove(mine)


def move(actual, x, y):
    """moving player basing on previous position on board, using getch()"""
    global BLOCKERS
    key = getch()
    actual.board[y][x] = " "
    if key == "a" and actual.board[y][x-1] not in BLOCKERS:
        x -= 1
    elif key == "d" and actual.board[y][x+1] not in BLOCKERS:
        x += 1
    elif key == "w" and actual.board[y-1][x] not in BLOCKERS:
        y -= 1
    elif key == "s" and actual.board[y+1][x] not in BLOCKERS:
        y += 1
    elif key == "h":
        show_pop_up(actual, HINTS)
    elif key == "m":
        sys.exit()
    elif key == "e":
        react(actual, x, y)
    else:
        pass
    return x, y


def show_pop_up(actual, dictionary, level='0'):
    board_copy = []
    for item in actual.board:
        board_copy.append(item[:])
    show_hint = choice(dictionary['0'])
    pop_height, pop_width = 5, len(show_hint[0])+4
    help_list = list(show_hint[0])
    x_start = 50 - pop_width//2
    x_end = x_start+pop_width+2
    for line in range(pop_height):
        if line in [0, pop_height-1]:
            board_copy[15+line][x_start:x_end] = ["#" for column in range(1, pop_width+3)]
        elif line in [1, pop_height-2]:
            board_copy[15+line][x_start:x_end] = ["#"] + [" " for column in range(2, pop_width+2)] + ["#"]
        else:
            board_copy[15+line][x_start:x_end] = ["#"] + [" "]*2 + help_list + [" "]*2 + ["#"]
    print_board(board_copy)
    sleep(1)


def main():
    height, width = 39, 100
    actual = maps_instantions[0]
    pos = 36, 13
    hero = create_hero()
    insert_player(actual, pos[0], pos[1])
    print_board(actual.board)
    while True:
        pos = move(actual, pos[0], pos[1])
        insert_player(actual, pos[0], pos[1], detector=True)
        print_board(actual.board)


if __name__ == '__main__':
    main()
