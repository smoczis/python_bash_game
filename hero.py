import os
import operator
import random
from re import match
from time import sleep
from text_in_out import *
from items import *
from maps_creator import *


class Hero:

    items_to_boxes = ['flag'] * 10 + ['dynamite'] * 10 + ['armour'] * 2 + ['chemical_suit'] * 1 + ['vaccine'] * 5 + ['metal_detector'] * 1
    hints_to_boxes = [('hint', 'A'), ('hint', 'B'), ('hint', 'C'), ('hint', 'N1'), ('hint', 'N2'), ('hint', 'N3')]
    boxes = [Box(item) for item in items_to_boxes]
    boxes += [Box(item, specification) for item, specification in hints_to_boxes]

    bombs_to_put = ['A', 'A', 'B', 'B', 'C', 'C', 'N']
    bombs = [Bomb(item) for item in bombs_to_put]

    def __init__(self):
        self.place = Item.maps_instantions['map0']
        self.background_char = ' '
        self.position = 1, 12
        self.exp = 0
        self.level = 1
        self.detect_range = 1
        self.backpack_capicity = 12
        self.alive = True
        self.score = 0
        self.notepad = []

    def get_player_name(self):
        self.name = pop_up(self.place.board,
                           ['Enter your name', 'Press space to finish typing:', ' '], ask=True).upper()

    def choose_equipment(self):
        with open('texts/equipment.txt', 'r', newline='\n') as text_file:
            text_file = text_file.readlines()
            equipment_intro = [line[:-1] for line in text_file[:6]]
            equipment_menu = [line[:-1] for line in text_file[8:16]]
        for_more_info = {'q': 'dynamite', 'w': 'metal_detector',
                         'e': 'chemical_suit', 'r': 'armour',
                         't': 'flag', 'y': 'vaccine'}
        pop_up(self.place.board, equipment_intro)
        backpack = []
        self.backpack_space = self.backpack_capicity
        ready = False
        shift_to_numbers = {'!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6'}
        while not ready:
            choose = pop_up(self.place.board, equipment_menu +
                            [' ', "You've taken: ", ' ', *backpack, ' ',
                             'You still can pack ' + str(self.backpack_space) + ' kg'])
            if choose.lower() in for_more_info:
                pop_up(self.place.board, Item.info[for_more_info[choose.lower()]])
            elif choose in shift_to_numbers.values():
                index = int(choose) - 1
                if Item.EQUIPMENT_WEIGHT[Item.EQUIPMENT[index]] <= self.backpack_space:
                    backpack.append(Item.EQUIPMENT[index])
                    self.backpack_space -= Item.EQUIPMENT_WEIGHT[Item.EQUIPMENT[index]]
                else:
                    pop_up(self.place.board, ["You don't have so much space for that item!"], auto_hide=1)
            elif choose in shift_to_numbers:
                index = int(shift_to_numbers[choose]) - 1
                if Item.EQUIPMENT[index] in backpack:
                    backpack.remove(Item.EQUIPMENT[index])
                    self.backpack_space += Item.EQUIPMENT_WEIGHT[Item.EQUIPMENT[index]]
                else:
                    pop_up(self.place.board, ["You can not drop something you don't have!"], auto_hide=1)
            elif choose == '\r':
                ready = True
            else:
                pop_up(self.place.board, ['Wrong choose!'], auto_hide=1)
        self.backpack = [Equipment(item) for item in backpack]

    def insert_on_board(self):
        """inserting player on board on given position. set see distance and makes visible hidden objects in that range
           also starts a reaction to players steping on / into sth"""
        numbers = [str(x) for x in range(10)]
        self.place.hide_mines()
        self.detect_mines()
        if self.position in self.place.mines:
            self.make_boom(self.position)
        elif self.position[0] in [0, 105] or self.position[1] in [0, 32]:
            self.change_map()
        elif self.place.board[self.position[1]][self.position[0]] == '`':
            if any([item.type == 'vaccine' for item in self.backpack]):
                self.place.board[self.position[1]][self.position[0]] = "@"
            else:
                pop_up(self.place.board, ['You have been killed by viruses'], auto_hide=1)
                pop_up(self.place.board, ['GAME OVER'], auto_hide=1)
                self.alive = False
        elif self.place.board[self.position[1]][self.position[0]] == '~':
            if any([item.type == 'chemical_suit' for item in self.backpack]):
                self.place.board[self.position[1]][self.position[0]] = "@"
            else:
                pop_up(self.place.board, ['You have been killed by poisonous gas'], auto_hide=1)
                pop_up(self.place.board, ['GAME OVER'], auto_hide=1)
                self.alive = False

        else:
            self.place.board[self.position[1]][self.position[0]] = "@"

    def move(self, key):
        """moving player basing on previous position on board, using getch()"""
        numbers = [str(x) for x in range(10)]
        x, y = self.position
        self.place.board[y][x] = self.background_char
        if key == "a" and self.place.board[y][x - 1] not in Maps.BLOCKERS:
            x -= 1
        elif key == "d" and self.place.board[y][x + 1] not in Maps.BLOCKERS:
            x += 1
        elif key == "w" and self.place.board[y - 1][x] not in Maps.BLOCKERS:
            y -= 1
        elif key == "s" and self.place.board[y + 1][x] not in Maps.BLOCKERS:
            y += 1
        self.background_char = self.place.board[y][x]
        self.position = x, y

    def browse_backpack(self):
        keys = [str(i + 1) for i in range(len(self.backpack))]
        backpack = {key: item for key, item in zip(keys, self.backpack)}
        browser_header = ['Your backpack:', ' ']
        browser_footer = [' ', 'You have got ' + str(self.backpack_space) + ' kg free space in backpack', ' ',
                          'Press item number for further actions', 'ENTER to go back to game']
        browsing_backpack = True
        while browsing_backpack:
            list_from_backpack = [key + ' - ' + backpack[key].type for key in keys]
            key = pop_up(self.place.board, browser_header + list_from_backpack + browser_footer)
            if key in keys:
                action = pop_up(self.place.board, backpack[key].info + [' ', 'press E to put item on filed'])
                if action.upper() == 'E':
                    self.put_item(backpack[key])
                    del backpack[key]
                    browsing_backpack = False
            elif key == '\r':
                browsing_backpack = False
            else:
                pop_up(self.place.board, ['Wrong key!'], auto_hide=1)

    def detect_mines(self):
        """showing on board all hidden objects in distance
           (calculated by calc_neighbours) of player's position. return board"""
        detect_range = self.detect_range
        for item in self.backpack:
            if item.type == 'metal_detector':
                detect_range = 5
        neighbours = calc_neighbours(self.position, detect_range)
        for (x, y) in neighbours:
            if (x, y) in self.place.mines:
                self.place.board[y][x] = "X"

    def detonate_dynamite(self):
        """detonating all dynamite put before"""
        objects_to_remove = []
        for item in self.place.objects:
            if item.type == 'dynamite':
                self.make_boom(item.position)
                objects_to_remove.append(item)
        for objects in objects_to_remove:
            objects.hide_on_board()

    def set_position(self, coordinate, side):
        if side == 'N':
            self.position = coordinate, 30
        elif side == 'S':
            self.position = coordinate, 2
        elif side == 'W':
            self.position = 103, coordinate
        elif side == 'E':
            self.position = 0, coordinate

    def change_map(self):
        if self.position[0] == 105:
            side = 'E'
            coordinate = (self.position[1])
        elif self.position[0] == 0:
            side = 'W'
            coordinate = (self.position[1])
        elif self.position[1] == 0:
            side = 'N'
            coordinate = (self.position[0])
        elif self.position[1] == 32:
            side = 'S'
            coordinate = (self.position[0])
        for maps in list(Item.maps_instantions):
            print(self.place.name)
            if maps == self.place.neighbour_maps[side]:
                self.place = Item.maps_instantions[maps]
                break
        self.set_position(coordinate, side)

    def disarm_mine(self):
        for cell in calc_neighbours(self.position):
            if cell in self.place.mines:
                self.place.mines.remove(cell)
                self.exp += 1

    def pick_item(self, item):
        if self.backpack_space < Item.EQUIPMENT_WEIGHT[item.type]:
            pop_up(self.place.board, ["You don't have so much space for that item!"], auto_hide=1)
        else:
            self.backpack.append(item)
            self.backpack_space -= Item.EQUIPMENT_WEIGHT[item.type]
            item.hide_on_board()

    def put_item(self, item):
        self.place.board[self.position[1]][self.position[0]] = item.char
        self.background_char = item.char
        print_board(self.place.board, self)
        item.place = self.place
        if item in self.backpack:
            item.position = self.position
            self.backpack.remove(item)
            self.backpack_space += Item.EQUIPMENT_WEIGHT[item.type]
            item.put_on_board()
        else:
            pop_up(self.place.board, ["You cannot put something you don't have!"], auto_hide=1)

    def react_with_object(self):
        objects_to_react = []
        for item in self.place.objects:
            if item.large > 0:
                if any([object_position in calc_neighbours(self.position) for object_position in item.position]):
                    objects_to_react.append(item)
            else:
                if item.position in calc_neighbours(self.position):
                    objects_to_react.append(item)
        print(objects_to_react)
        if objects_to_react:
            if objects_to_react[0].type == 'bomb':
                self.disarm_bomb(objects_to_react[0])
            elif objects_to_react[0].type == 'box':
                objects_to_react[0].open()
            elif objects_to_react[0].type == 'hint':
                self.take_hint(objects_to_react[0])
            else:
                self.pick_item(objects_to_react[0])
        else:
            self.disarm_mine()

    def take_hint(self, hint):
        for item in hint.content:
            self.notepad.append(item)
        self.notepad.append(' ')
        hint.hide_on_board()

    def display_notepad(self):
        pop_up(self.place.board, ['Hints you have collected:', ' '] + [note for note in self.notepad])

    def disarm_bomb(self, bomb):
        if bomb.is_armed:
            bomb.guess_number(self)

    def make_boom(self, position, power=5, is_deadly=True):
        """making explosion in given position, power is radius of near fields to be destroyed"""
        field_of_fire = calc_neighbours(position, distance=power)
        board_copy = [item[:] for item in self.place.board]
        for i in range(power):
            for cell in calc_neighbours(position, i):
                board_copy[cell[1]][cell[0]] = '#'
            print_board(board_copy)
            sleep(0.05)
        for cell in field_of_fire:
            if self.place.board[cell[1]][cell[0]] not in Maps.BOOM_PROOF:
                self.place.board[cell[1]][cell[0]] = ' '
            if cell in self.place.mines:
                self.place.mines.remove(cell)
        if self.position in field_of_fire and is_deadly:
            if any([item.type == 'armour' for item in self.backpack]):
                for item in self.backpack:
                    if item.type == 'armour':
                        self.backpack.remove(item)
                        self.backpack_space += Item.EQUIPMENT_WEIGHT[item.type]
                        break
                self.place.board[self.position[1]][self.position[0]] = '@'
                print_board(self.place.board)
            else:
                pop_up(self.place.board, ["You have been killed by exlosion"], auto_hide=1)
                pop_up(self.place.board, ["GAME OVER"], auto_hide=1)
                self.alive = False
        print_board(self.place.board)

    def celebrate_win(self):
        pop_up(self.place.board, read_from_text('win.txt'))
        positions = [generate_random_position(self.place.board) for i in range(20)]
        for position in positions:
            self.make_boom(position, is_deadly=False)
        self.alive = False
