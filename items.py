import random
from maps_creator import *
from text_in_out import *


class Item:

    info = load_info('equipment')

    def set_position(self, large):
        ready = False
        while not ready:
            start = (random.randint(2, (len(self.place.board[0]) - 4)),
                     random.randint(2, (len(self.place.board) - 4)))
            self.position = calc_neighbours(self.place, start[0], start[1], distance=large)
            if all([self.place.board[y][x] == ' ' for x, y in self.position]):
                ready = True

#        elif self.item_type = 'bomb':
#            self.char = COLOURS['F']

    def put_on_board(self):
        self.place.objects.append(self)
        if self.large > 0:
            for x, y in self.position:
                self.place.board[y][x] = self.char
        else:
            x, y = self.position
            self.place.board[y][x] = self.char


class Box(Item):
    """docstring for Item ."""

    def __init__(self, content):
        self.type = 'box'
        self.char = COLOURS['T']
        self.large = 1
        self.place = maps_instantions[random.randint(0, (len(maps_instantions)-1))]
        self.set_position(self.large)
        self.opened = False
        self.content = Equipment(content)
        self.put_on_board()

    def open(self):
        if not self.opened:
            for x, y in self.position:
                self.place.board[y][x] = ' '
            self.content.place = self.place
            self.content.position = self.position[1]
            self.content.put_on_board()
            self.opened = True


class Equipment(Item):
    def __init__(self, content):
        self.type = content
        self.large = 0
        self.set_char_look()
        self.info
        self.info = Item.info[self.type]

    def set_char_look(self):
        if self.type == 'dynamite':
            self.char = '⌫'
        elif self.type == 'metal_detector':
            self.char = '♩'
        elif self.type == 'chemical_suit':
            self.char = 'C'
        elif self.type == 'armour':
            self.char = 'A'
        elif self.type == 'flag':
            self.char = '⚑'
        elif self.type == 'vaccine':
            self.char = '💉'

    def hide_on_board(self):
        self.place.board[self.position[1]][self.position[0]] = ' '
