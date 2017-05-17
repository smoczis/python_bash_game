import os
import sys
import random
import time
from maps_creator import *
from hero import *
from files_operations import *
from text_in_out import *
from items import *
from hot_cold_game import *

PLAYER_OBJ_COLOURS = {'dynamite': COLOURS['C'], 'flag': COLOURS['F']}
BOOM_PROOF = [COLOURS['N'], COLOURS['V']]
BLOCKERS = [COLOURS['X'], COLOURS['G'], COLOURS['N'], COLOURS['C'], COLOURS['F'],
            COLOURS['T'], COLOURS['S'], COLOURS['N'], COLOURS['V']]


boxes = []

HINTS = {
        '0': [("Type the capital of Poland", "Warsaw"), ("Type the capital of France", "Paris"),
              ("Dupa cycki lasery", "Dzoana Krupa")],
        '1': ['Type the factorial of number 3', '6'],
        '2': ['What the \'int\' abbreviate for?', 'integer']
}



def menu(actual):
    key = pop_up(actual.board, ['to save press S', 'to exit press Q'])
    if key == 'q':
        game_on = False
    else:
        pop_up(actual.board, ['wrong!'], auto_hide=1)


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
    numbers = [str(x) for x in range(10)]
    if detector:
        see_distance = 5
    else:
        see_distance = 1
    hide_mines(actual)
    neighbours = calc_neighbours(actual, actual.player_position[0], actual.player_position[1], see_distance)
    show_neighbours(actual, neighbours)
    if actual.player_position in actual.mines:
        game_on = boom(actual, actual.player_position[0], actual.player_position[1])
    elif actual.board[actual.player_position[1]][actual.player_position[0]] in numbers:
        game_on = True
        change_actual()
    else:
        actual.board[actual.player_position[1]][actual.player_position[0]] = "@"
        game_on = True
    return game_on


def change_actual(actual):
    if actual.player_position[0] in [0, 105]:
        portal = ('y', actual.player_position[1])
    else:
        portal = ('x', actual.player_position[0])
    previous = str(maps_instantions.index(actual))
    actual = maps_instantions[int(actual.board[actual.player_position[1]][actual.player_position[0]])]
    actual.start_position(portal, previous)
    return actual


def react(actual, x, y):
    """reacting to neighbour item"""
    for cell in calc_neighbours(actual, x, y):
        if cell in actual.mines:
            actual.mines.remove(cell)
            hero['exp'] += 1
            break
        elif cell in actual.player_objects:
            hero[actual.player_objects[cell]] += 1
            del actual.player_objects[cell]
            actual.board[cell[1]][cell[0]] = ' '
        else:
            for box in boxes:
                if not box.opened:
                    for pos in box.position:
                        if box.place == actual and pos == cell:
                            box.open()


def put(actual, item, x, y):
    """droping item from equipment next to players actual position"""
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


def detonate_dynamite(actual):
    """detonating all dynamite put before"""
    objects_to_remove = []
    for cell in actual.player_objects:
        if actual.player_objects[cell] == 'dynamite':
            game_on = boom(actual, cell[0], cell[1])
            objects_to_remove.append(cell)
    for objects in objects_to_remove:
        del actual.player_objects[objects]
    return game_on


def boom(actual, x, y, power=5):
    """making explosion in given position, power is radius of near fields to be destroyed"""
    field_of_fire = calc_neighbours(actual, x, y, power)
    field_of_fire.append((x, y))
    board_copy = [item[:] for item in actual.board]
    for i in range(power):
        for cell in calc_neighbours(actual, x, y, i):
            board_copy[cell[1]][cell[0]] = '#'
        print_board(board_copy)
        sleep(0.05)
    for cell in field_of_fire:
        if actual.board[cell[1]][cell[0]] not in BOOM_PROOF:
            actual.board[cell[1]][cell[0]] = ' '
        if cell in actual.mines:
            actual.mines.remove(cell)
    if actual.player_position in field_of_fire:
        print('yes')
        game_on = False
    print_board(actual.board)
    return game_on


def move(actual):
    """moving player basing on previous position on board, using getch()"""
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
        sero = pop_up(actual.board, ['jajca jak berety, jak zadziała to superekstra zajebiście', 'kamaz', 'dupa', 'bazary czy prokreacja?'], ask=True)
        pop_up(actual.board, [sero])
    elif key == "n":
        sys.exit()
    elif key == "e":
        react(actual, x, y)
    elif key == "q":
        put(actual, 'dynamite', x, y)
    elif key == "f":
        put(actual, 'flag', x, y)
    elif key == "b":
        detonate_dynamite(actual)
    elif key == "p":
        zero = hot_cold(actual.board, 10, 15, is_even=True)
    elif key == "m":
        menu(actual)
    actual.player_position = x, y


def endgame(actual):
    pop_up(actual.board, ['konec'], auto_hide=2)
    os.system('clear')


def main():
    global boxes
    maps_instantions = load_maps('maps')
    actual = maps_instantions[0]
    actual.player_position = 28, 5
    backpack = choose_eq(actual, 12)
    eq = ['flag', 'flag', 'flag']
    for item in eq:
        boxes.append(Box(item))
    print_board(actual.board)
    game_on = True
    while game_on:
        game_on = insert_player(actual, detector=True)
        print_board(actual.board)
        for box in boxes:
            print(actual, box.position)
        move(actual)
    endgame(actual)


if __name__ == '__main__':
    main()
