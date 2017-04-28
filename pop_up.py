from game import *


def show_pop_up(board, dictionary, level='0'):
    board_copy = board
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
    return board_copy
