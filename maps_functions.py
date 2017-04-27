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
