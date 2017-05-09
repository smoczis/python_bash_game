import os
import sys
import tty
import termios
import random
import time
from re import match
from maps_creator import *
from hero import *

player_objects = {'dynamite': COLOURS['C'], 'flag': COLOURS['F']}
BLOCKERS = [COLOURS['X'], COLOURS['G'], COLOURS['N'], COLOURS['C'], COLOURS['F'], COLOURS['T'], COLOURS['S']]


HINTS = {
        '0': [("Type the capital of Poland", "Warsaw"), ("Type the capital of France", "Paris"),
              ("Dupa cycki lasery", "Dzoana Krupa")],
        '1': ['Type the factorial of number 3', '6'],
        '2': ['What the \'int\' abbreviate for?', 'integer']
}

game_on = True


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


def insert_player(actual, detector=False):
    """inserting player on board on given position. set see distance and makes visible hidden objects in that range
       also starts a reaction to players steping on / into sth"""
    global COLOURS
    numbers = [str(x) for x in range(10)]
    if detector:
        see_distance = 5
    else:
        see_distance = 1
    hide_mines(actual)
    neighbours = calc_neighbours(actual, actual.player_position[0], actual.player_position[1], see_distance)
    show_neighbours(actual, neighbours)
    if actual.player_position in actual.mines:
        boom(actual, actual.player_position[0], actual.player_position[1])
    elif actual.board[actual.player_position[1]][actual.player_position[0]] in numbers:
        previous = str(maps_instantions.index(actual))
        actual = maps_instantions[int(actual.board[actual.player_position[1]][actual.player_position[0]])]
        actual.start_position(previous)
    else:
        actual.board[actual.player_position[1]][actual.player_position[0]] = "@"
    return actual


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
    """reacting to neighbour item"""
    global hero
    for cell in calc_neighbours(actual, x, y):
        if cell in actual.mines:
            actual.mines.remove(cell)
            hero['exp'] += 1
            break
        elif (cell[0], cell[1], 'flag') in actual.player_objects:
            actual.player_objects.remove((cell[0], cell[1], 'flag'))
            actual.board[cell[1]][cell[0]] = ' '
            hero['flag'] += 1
        elif (cell[0], cell[1], 'dynamite') in actual.player_objects:
            actual.player_objects.remove((cell[0], cell[1], 'dynamite'))
            actual.board[cell[1]][cell[0]] = ' '
            hero['dynamite'] += 1


def put(item, actual, x, y):
    """droping item from equipment next to players actual position"""
    item = item.lower()
    if hero[item] > 0:
        actual.board[y][x] = player_objects[item]
        print_board(actual.board)
        key = getch()
        if key == "a" and actual.board[y][x-1] not in BLOCKERS:
            x -= 1
        elif key == "d" and actual.board[y][x+1] not in BLOCKERS:
            x += 1
        elif key == "w" and actual.board[y-1][x] not in BLOCKERS:
            y -= 1
        elif key == "s" and actual.board[y+1][x] not in BLOCKERS:
            y += 1
        actual.board[y][x] = player_objects[item]
        actual.player_objects.append((x, y, item))
        hero[item] -= 1
    else:
        pass


def detonate_dynamite(actual):
    """detonating all dynamite put before"""
    for cell in actual.player_objects:
        if cell[2] == 'dynamite':
            boom(actual, cell[0], cell[1])
            actual.player_objects.remove(cell)


def boom(actual, x, y, power=5):
    """making explosion in given position, power is radius of near fields to be destroyed"""
    global game_on
    field_of_fire = calc_neighbours(actual, x, y, power)
    field_of_fire.append((x, y))
    print(field_of_fire, actual.player_position)
    for i in range(power):
        for cell in calc_neighbours(actual, x, y, i):
            actual.board[cell[1]][cell[0]] = '#'
        print_board(actual.board)
        sleep(0.05)
    for cell in field_of_fire:
        actual.board[cell[1]][cell[0]] = ' '
        if cell in actual.mines:
            actual.mines.remove(cell)
    if actual.player_position in field_of_fire:
        print('yes')
        game_on = False
    print_board(actual.board)


def move(actual):
    """moving player basing on previous position on board, using getch()"""
    global BLOCKERS
    numbers = [str(x) for x in range(10)]
    key = getch()
    x, y = actual.player_position[:]
    if actual.board[y][x] not in numbers:
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
    elif key == "q":
        put('dynamite', actual, x, y)
    elif key == "f":
        put('flag', actual, x, y)
    elif key == "b":
        detonate_dynamite(actual)
    actual.player_position = x, y
    return actual.player_position


def show_pop_up(actual, dictionary, level='0'):
    board_copy = []
    for item in actual.board:
        board_copy.append(item[:])
    show_hint = random.choice(dictionary['0'])
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


def endgame():
    print('konec')


def main():
    global game_on
    global footer
    global hero
    height, width = 39, 100
    map_number = 0
    actual = maps_instantions[map_number]
    hero = create_hero()
    footer = create_footer(hero)
    actual.player_position = 36, 13
    print_board(actual.board)
    while game_on:
        actual = insert_player(actual, detector=True)
        footer = create_footer(hero)
        print_board(actual.board)
        print(actual, actual.player_position, actual.player_objects)
        move(actual)
    endgame()


if __name__ == '__main__':
    main()
