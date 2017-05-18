import random
import sys
import os


def print_board(board):
    """printing given board on screen. before that adjust screen size, and clear previous prints"""
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=107))
    os.system('clear')
    for line in board:
        print("".join(line))


class Maps:
    """class for maps"""
    def __init__(self, plik):
        self.board = []
        self.mines = []
        self.import_map(plik)
        self.colour_map(self.board)
        self.put_mines(20)

    def put_mines(self, quantity):
        """randomly selecting positions of given quantity of mines. returns a list of tuples (x, y)"""
        while len(self.mines) < quantity:
            y = random.randint(0, len(self.board)-1)
            x = random.randint(0, len(self.board[0])-1)
            if self.board[y][x] == ' ':
                self.mines.append((x, y))

    def import_map(self, mapa):
        # maybe using try and finally?
        with open(mapa, 'r', newline='\n') as map_file:
            for line in map_file:
                self.board.append([char for char in line[:-1]])

    def colour_map(self, board):
        COLOURS = {'X': '\x1b[0;31;41m'+'X'+'\x1b[0m',
                   'G': '\x1b[0;32;42m'+'G'+'\x1b[0m',
                   'N': '\x1b[0;34;44m'+'N'+'\x1b[0m'}
        for line_i in range(len(self.board)):
            for char_i in range(len(self.board[line_i])):
                if self.board[line_i][char_i] in COLOURS.keys():
                    self.board[line_i][char_i] = COLOURS[self.board[line_i][char_i]]


maps_instantions = []
"""making maps as Map class instances using every file in /maps directotry which is .txt
   and storing it to list of instances"""
for f in os.listdir("maps"):
    if f.endswith(".txt"):
        maps_instantions.append(Maps('maps/' + f))
