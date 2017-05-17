import random
import sys
import os


COLOURS = {'X': '\x1b[0;37;41m' + ' ' + '\x1b[0m',  # red
           'G': '\x1b[0;37;42m' + ' ' + '\x1b[0m',  # green
           'N': '\x1b[0;37;44m' + ' ' + '\x1b[0m',  # blue
           'C': '\x1b[0;37;40m' + ' ' + '\x1b[0m',  # black
           'F': '\x1b[0;30;47m' + ' ' + '\x1b[0m',  # white
           'T': '\x1b[0;37;43m' + ' ' + '\x1b[0m',  # gold
           'V': '\x1b[5;30;42m' + ' ' + '\x1b[0m',  # green BOOM_PROOF
           'S': '\x1b[0;37;46m' + ' ' + '\x1b[0m'
           }
# \x1b is a single char!
maps_instantions = []


def print_text(board, x, y, text):
    for i, char in enumerate(text):
        board[y][x + i] = char
    return board


def create_footer():
    footer = []
    for line in range(3):
        footer.append([' ' for i in range(106)])
    line_length = 0
    for item in ['1 - BACKPACK', '2 - INSTRUCTIONS', '3 - CONTROLS', '4 - EXIT GAME']:
        print_text(footer, line_length + 3, 1, item)
        line_length += len(item) + 3
    return footer


def print_board(board):
    footer = create_footer()
    """printing given board on screen. before that adjust screen size, and clear previous prints"""
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=106))
    os.system('clear')
    for line in board:
        print(''.join(line))
    for line in footer:
        for i in range(len(line)):
            line[i] = '\x1b[0;37;40m' + line[i] + '\x1b[0m'
        print(''.join(line))


class Maps:
    """class for maps"""
    def __init__(self, map_file):
        self.board = []
        self.mines = []
        self.player_objects = {}
        self.player_position = None
        self.import_map(map_file)
        self.colour_map(self.board)
        self.put_mines(20)

    def put_mines(self, quantity):
        """randomly selecting positions of given quantity of mines. returns a list of tuples (x, y)"""
        while len(self.mines) < quantity:
            y = random.randint(0, len(self.board)-1)
            x = random.randint(0, len(self.board[0])-1)
            if self.board[y][x] == ' ' and (x, y) != (28, 5):
                self.mines.append((x, y))

    def start_position(self, portal, previous):
        if portal[0] == 'x':
            for line_i in range(len(self.board)):
                if self.board[line_i][portal[1]] == previous:
                    self.player_position = portal[1], line_i
        else:
            for char_i in range(len(self.board[portal[1]])):
                if self.board[portal[1]][char_i] == previous:
                    self.player_position = char_i, portal[1]

    def import_map(self, map_file):
        with open(map_file, 'r', newline='\n') as map_file:
            for line in map_file:
                self.board.append([char for char in line[:-1]])

    def colour_map(self, board):
        for line_i in range(len(self.board)):
            for char_i in range(len(self.board[line_i])):
                if self.board[line_i][char_i] in COLOURS.keys():
                    self.board[line_i][char_i] = COLOURS[self.board[line_i][char_i]]



def load_maps(catalog):
    """making maps as Map class instances using every file in /maps directotry which is .txt
       and storing it to list of instances"""
    for map_file in os.listdir("maps"):
        if map_file.endswith(".txt"):
            maps_instantions.append(Maps(catalog + '/' + map_file))
    return maps_instantions
