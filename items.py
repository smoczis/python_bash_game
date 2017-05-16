import random
from maps_creator import *


class Box:
    """docstring for Item ."""
    global maps_instantions
    global COLOURS

    def __init__(self, equipment):
        self.place = maps_instantions[random.randint(0, (len(maps_instantions)-1))]
        self.set_position()
        self.opened = False
        self.equipment = equipment
        self.insert()

    def set_position(self):
        ready = False
        while not ready:
            start = (random.randint(2, (len(self.place.board[0]) - 4)),
                     random.randint(2, (len(self.place.board) - 4)))
            self.position = []
            for delta_y in range(2):
                for delta_x in range(2):
                    if self.place.board[start[1] + delta_y][start[0] + delta_x] == ' ':
                        self.position.append((start[0] + delta_x, start[1] + delta_y))
                        ready = True
                    else:
                        ready = False

    def insert(self):
        for x, y in self.position:
            self.place.board[y][x] = COLOURS['T']

    def open(self):
        for x, y in self.position:
            self.place.board[y][x] = ' '
        self.place.board[self.position[0][1]][self.position[0][0]] = 'E'
        self.place.player_objects[self.position[0]] = self.equipment
        self.opened = True
