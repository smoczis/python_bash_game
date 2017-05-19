import random
import sys
import os


def insert_text(board, x, y, text, background=None):
    if background is None:
        prefix = ''
        suffix = ''
    else:
        prefix = background[:10]
        suffix = background[-4:]
    for i, char in enumerate(str(text)):
        board[y][x + i] = prefix + char + suffix
    return board


def create_footer(player):
    footer = []
    for line in range(5):
        footer.append([' ' for i in range(106)])
    if player:
        line_length = 0
        for item in ['1 - BACKPACK', '2 - INSTRUCTIONS', '3 - CONTROLS', '4 - EXIT GAME']:
            insert_text(footer, line_length + 3, 1, item)
            line_length += len(item) + 15
        line_length = 0
        for item in ['PLAYER: ' + player.name, 'EXP: ' + str(player.exp), 'SCORE: ' + str(player.score)]:
            insert_text(footer, line_length + 3, 3, item)
            line_length += len(item) + 10
    return footer


def print_board(board, player=None):
    """printing given board on screen. before that adjust screen size, and clear previous prints"""
    footer = create_footer(player)
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=106))
    os.system('clear')
    for line in board:
        print(''.join(line))
    for line in footer:
        for i in range(len(line)):
            line[i] = '\x1b[0;37;40m' + line[i] + '\x1b[0m'
        print(''.join(line))


def calc_neighbours(position, distance=1):
    """calculating and set to list all board cells in given distance (default 1) from x, y"""
    neighbours = []
    x, y = position
    for delta_y in range(-distance, distance + 1):
        for delta_x in range(-distance, distance + 1):
            if y + delta_y in range(33) and x + delta_x in range(106):
                neighbours.append((x + delta_x, y + delta_y))
    return neighbours


def load_maps(catalog):
    """making maps as Map class instances using every file in /maps directotry which is .txt
       and storing it to list of instances"""
    map_files = [f for f in os.listdir("maps")]
    map_files = sorted(map_files)
    maps_instantions = {}
    for map_file in map_files:
        if map_file.endswith(".txt"):
            maps_instantions[map_file.split('.')[0]] = Maps(catalog + '/' + map_file)
    return maps_instantions


class Maps:
    """class for maps"""

    COLOURS = {'X': '\x1b[0;37;41m' + ' ' + '\x1b[0m',  # red
               'G': '\x1b[0;37;42m' + ' ' + '\x1b[0m',  # green
               'N': '\x1b[0;37;44m' + ' ' + '\x1b[0m',  # blue
               'C': '\x1b[0;37;40m' + ' ' + '\x1b[0m',  # black
               'F': '\x1b[0;30;47m' + ' ' + '\x1b[0m',  # white
               'T': '\x1b[0;37;43m' + ' ' + '\x1b[0m',  # gold
               'V': '\x1b[5;30;42m' + ' ' + '\x1b[0m',  # green BOOM_PROOF
               'S': '\x1b[0;37;46m' + ' ' + '\x1b[0m',
               'D': '\x1b[5;37;41m' + ' ' + '\x1b[0m',   # destroyable green
               'M': '\x1b[0;36;46m' + ' ' + '\x1b[0m'
               }

    BLOCKERS = [COLOURS['X'], COLOURS['G'], COLOURS['N'], COLOURS['C'], COLOURS['F'],
                COLOURS['T'], COLOURS['S'], COLOURS['N'], COLOURS['V']]

    BOOM_PROOF = [COLOURS['N'], COLOURS['V'], COLOURS['X'], COLOURS['T'], COLOURS['F']]

    def __init__(self, map_file):
        self.name = map_file
        self.board = []
        self.mines = []
        self.objects = []
        self.neighbour_maps = {}
        self.import_map(map_file)
        self.colour_map(self.board)
        self.put_mines(20)

    def put_mines(self, quantity):
        """randomly selecting positions of given quantity of mines. returns a list of tuples (x, y)"""
        while len(self.mines) < quantity:
            y = random.randint(2, len(self.board)-3)
            x = random.randint(2, len(self.board[0])-3)
            if self.board[y][x] == ' ':
                self.mines.append((x, y))

    def hide_mines(self):
        """hiding all mines, that were printed before by show_neighbours()"""
        for line_i in range(len(self.board)):
            for char_i in range(len(self.board[line_i])):
                if self.board[line_i][char_i] == 'X':
                    self.board[line_i][char_i] = ' '

    def import_map(self, map_file):
        with open(map_file, 'r', newline='\n') as map_file:
            map_file = map_file.readlines()
            for line in map_file[:-1]:
                self.board.append([char for char in line[:-1]])
            for item in map_file[-1][:-1].split(','):
                self.neighbour_maps[item.split(':')[0]] = item.split(':')[1]

    def colour_map(self, board):
        for line_i in range(len(self.board)):
            for char_i in range(len(self.board[line_i])):
                if self.board[line_i][char_i] in Maps.COLOURS.keys():
                    self.board[line_i][char_i] = Maps.COLOURS[self.board[line_i][char_i]]
