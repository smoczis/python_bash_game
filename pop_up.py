def show_pop_up(board, dictionary, level='0'):
    board_copy = board[:]
    show_hint = choice(dictionary['0'])
    pop_height, pop_width = 5, len(show_hint[0])+4
    help_list = list(show_hint[0])
    pop_up_window = []
    x_start = 50 - pop_width//2
    x_end = x_start+pop_width+2
    for line in range(pop_height):
        if line in [0, pop_height-1]:
            board[15+line][x_start:x_end] = ["#" for column in range(1, pop_width+3)]
        elif line in [1, pop_height-2]:
            board[15+line][x_start:x_end] = ["#"] + [" " for column in range(2, pop_width+2)] + ["#"]
        else:
            board[15+line][x_start:x_end] = ["#"] + [" "]*2 + help_list + [" "]*2 + ["#"]
    print_board(board)
    sleep(2)
    board = board_copy[:]
    return board


#### copied from main file to see if module with class is working###


def import_map(map):
    with open(map, 'r', newline='\n') as map_file:
        board = []
        for line in map_file:
            board.append([char for char in line[:-1]])
    board = colour_map(board)
    return board


def colour_map(board):
    global COLOURS
    COLOURS = {'X': '\x1b[0;31;41m'+'X'+'\x1b[0m',
               'G': '\x1b[0;32;42m'+'G'+'\x1b[0m',
               'N': '\x1b[0;34;44m'+'N'+'\x1b[0m'}
    for line_i in range(len(board)):
        for char_i in range(len(board[line_i])):
            if board[line_i][char_i] in COLOURS.keys():
                board[line_i][char_i] = COLOURS[board[line_i][char_i]]
    return board


def print_board(board):
    """printing given board on screen. before that adjust screen size, and clear previous prints"""
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=107))
    os.system('clear')
    for line in board:
        print("".join(line))


def create_board(width, height):
    """creating empty board with frames of 'X'. given height and width. curently not in use"""
    width = int(width)
    height = int(height)
    board = []
    for line in range(1, height + 1):
        if line in [1, height]:
            board.append(["X" for column in range(1, width+1)])
        else:
            board.append(["X"] + [" " for column in range(2, width)] + ["X"])
    return board




class Mapa:
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
