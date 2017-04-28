def import_map(map):
    with open(map, 'r', newline='\n') as map_file:
        board = []
        for line in map_file:
            board.append([char for char in line[:-1]])
    board = colour_map(board)
    return board


def colour_map(board):
    global COLOURS
    COLOURS = {'X': '\x1b[0;31;41m'+'X'+'\x1b[0m', 'G': '\x1b[0;32;42m'+'G'+'\x1b[0m', 'N': '\x1b[0;34;44m'+'N'+'\x1b[0m'}
    for line_i in range(len(board)):
        for char_i in range(len(board[line_i])):
            if board[line_i][char_i] in COLOURS.keys():
                board[line_i][char_i] = COLOURS[board[line_i][char_i]]
    return board


def print_board():
    """printing given board on screen. before that adjust screen size, and clear previous prints"""
    global board
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
