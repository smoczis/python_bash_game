import os
import sys
import random
import time
from re import match
from maps_creator import *
from hero import *
from files_operations import *
from text_in_out import *


PLAYER_OBJ_COLOURS = {'dynamite': COLOURS['C'], 'flag': COLOURS['F']}
BLOCKERS = [COLOURS['X'], COLOURS['G'], COLOURS['N'], COLOURS['C'], COLOURS['F'], COLOURS['T'], COLOURS['S']]


HINTS = {
        '0': [("Type the capital of Poland", "Warsaw"), ("Type the capital of France", "Paris"),
              ("Dupa cycki lasery", "Dzoana Krupa")],
        '1': ['Type the factorial of number 3', '6'],
        '2': ['What the \'int\' abbreviate for?', 'integer']
}

game_on = True
actual = None


def pop_up(text_lines, auto_hide=0, ask=False, colour=COLOURS['C']):
    global actual
    global COLOURS
    board_copy = []
    pop_width = 0
    if ask:
        pop_height = 5 + len(text_lines)
    else:
        pop_height = 4 + len(text_lines)
    for item in actual.board:
        board_copy.append(item[:])
    for item in text_lines:
        if len(str(item)) > pop_width:
            pop_width = len(str(item)) + 4
    x_start = 50 - pop_width//2
    x_end = x_start+pop_width+2
    for line in range(15, 15 + pop_height):
        board_copy[line][x_start:x_end] = [colour for column in range(pop_width+2)]
    for i, item in enumerate(text_lines):
        print_text(board_copy, x_start + 3, 17 + i, item, background=colour)
    print_board(board_copy)
    if auto_hide > 0:
        sleep(auto_hide)
        result = None
    else:
        if ask:
            result = get_input(board_copy, x_start + 3, 17 + len(text_lines), '', background=colour)
        else:
            result = getch()
    return result


def menu():
    global game_on
    global actual
    global hero
    key = pop_up(['to save press S', 'to exit press Q'])
    if key == 's':
        save(actual, hero)
    elif key == 'q':
        game_on = False
    else:
        pop_up(['wrong!'], auto_hide=1)


def hide_mines():
    """hiding all mines, that were printed before by show_neighbours()"""
    global actual
    for line_i in range(len(actual.board)):
        for char_i in range(len(actual.board[line_i])):
            if actual.board[line_i][char_i] == 'X':
                actual.board[line_i][char_i] = ' '
    return actual.board


def calc_neighbours(x, y, distance=1):
    """calculating and set to list all board cells in given distance (default 1) from x, y"""
    global actual
    neighbours = []
    for delta_y in range(-distance, distance + 1):
        for delta_x in range(-distance, distance + 1):
            if y + delta_y in range(len(actual.board)) and x + delta_x in range(len(actual.board[0])):
                neighbours.append((x + delta_x, y + delta_y))
    return neighbours


def show_neighbours(neighbours):
    """showing on board all hidden objects in distance
       (calculated by calc_neighbours) of player's position. return board"""
    global actual
    for (x, y) in neighbours:
        if (x, y) in actual.mines:
            actual.board[y][x] = "X"
    return actual.board


def insert_player(detector=False):
    """inserting player on board on given position. set see distance and makes visible hidden objects in that range
       also starts a reaction to players steping on / into sth"""
    global COLOURS
    global actual
    numbers = [str(x) for x in range(10)]
    if detector:
        see_distance = 5
    else:
        see_distance = 1
    hide_mines()
    neighbours = calc_neighbours(actual.player_position[0], actual.player_position[1], see_distance)
    show_neighbours(neighbours)
    if actual.player_position in actual.mines:
        boom(actual.player_position[0], actual.player_position[1])
    elif actual.board[actual.player_position[1]][actual.player_position[0]] in numbers:
        if actual.player_position[0] in [0, 105]:
            portal = ('y', actual.player_position[1])
        else:
            portal = ('x', actual.player_position[0])
        previous = str(maps_instantions.index(actual))
        actual = maps_instantions[int(actual.board[actual.player_position[1]][actual.player_position[0]])]
        actual.start_position(portal, previous)
    else:
        actual.board[actual.player_position[1]][actual.player_position[0]] = "@"
    return actual


def react(x, y):
    """reacting to neighbour item"""
    global hero
    global actual
    for cell in calc_neighbours(x, y):
        if cell in actual.mines:
            actual.mines.remove(cell)
            hero['exp'] += 1
            break
        elif cell in actual.player_objects:
            hero[actual.player_objects[cell]] += 1
            del actual.player_objects[cell]
            actual.board[cell[1]][cell[0]] = ' '


def put(item, x, y):
    """droping item from equipment next to players actual position"""
    global actual
    item = item.lower()
    if hero[item] > 0:
        actual.board[y][x] = PLAYER_OBJ_COLOURS[item]
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
        actual.board[y][x] = PLAYER_OBJ_COLOURS[item]
        actual.player_objects[(x, y)] = item
        hero[item] -= 1
    else:
        pass


def detonate_dynamite():
    """detonating all dynamite put before"""
    global actual
    obj_to_remove = []
    for cell in actual.player_objects:
        if actual.player_objects[cell] == 'dynamite':
            boom(cell[0], cell[1])
            obj_to_remove.append(cell)
    for obj in obj_to_remove:
        del actual.player_objects[obj]


def boom(x, y, power=5):
    """making explosion in given position, power is radius of near fields to be destroyed"""
    global game_on
    global actual
    field_of_fire = calc_neighbours(x, y, power)
    field_of_fire.append((x, y))
    print(field_of_fire, actual.player_position)
    for i in range(power):
        for cell in calc_neighbours(x, y, i):
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


def move():
    """moving player basing on previous position on board, using getch()"""
    global BLOCKERS
    global actual
    global hero
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
        sero = pop_up(['jajca jak berety, jak zadziała to superekstra zajebiście', 'kamaz', 'dupa', 'bazary czy prokreacja?'], ask=True)
        pop_up([sero])
    elif key == "n":
        sys.exit()
    elif key == "e":
        react(x, y)
    elif key == "q":
        put('dynamite', x, y)
    elif key == "f":
        put('flag', x, y)
    elif key == "b":
        detonate_dynamite()
    elif key == "p":
        zero = get_input(actual.board, x, y, 'WPISZ COŚ: ')
        print_text(actual.board, x, y+5, zero)
    elif key == "m":
        menu()
    actual.player_position = x, y
    return actual.player_position


def endgame():
    pop_up(['konec'], auto_hide=2)
    os.system('clear')


def main():
    global game_on
    global footer
    global actual
    global maps_instantions
    global hero
#    height, width = 39, 100
#    actual = maps_instantions[0]
#    hero = create_hero()
#    actual.player_position = 36, 13
    actual, hero, actual.player_position = starter()
    footer = create_footer(hero)
    print_board(actual.board)
    while game_on:
        actual = insert_player(detector=True)
        footer = create_footer(hero)
        print_board(actual.board)
        print(hero, actual, actual.player_position, actual.player_objects)
        move()
    endgame()


if __name__ == '__main__':
    main()
