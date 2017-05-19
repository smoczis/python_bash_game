import sys
import tty
import termios
from maps_creator import *
import os
import random
from time import sleep


def getch():
    """read users input without pressing 'enter'. returns one (first) char of input"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch.lower()


def pop_up(board, text_lines, auto_hide=0, ask=False, ans_len=False, colour=Maps.COLOURS['C']):
    board_copy = []
    pop_width = 0
    if ask:
        pop_height = 5 + len(text_lines)
    else:
        pop_height = 4 + len(text_lines)
    for item in board:
        board_copy.append(item[:])
    for item in text_lines:
        if len(str(item)) > pop_width:
            pop_width = len(str(item)) + 4
    x_start = 50 - pop_width // 2
    x_end = x_start+pop_width + 2
    for line in range(5, 5 + pop_height):
        board_copy[line][x_start:x_end] = [colour for column in range(pop_width+2)]
    for i, item in enumerate(text_lines):
        insert_text(board_copy, x_start + 3, 7 + i, item, background=colour)
    print_board(board_copy)
    if auto_hide > 0:
        sleep(auto_hide)
        result = None
    else:
        if ask:
            result = get_input(board_copy, x_start + 3, 7 + len(text_lines), '', ans_len=ans_len, background=colour)
        else:
            result = getch()
    return result


def get_input(board, x, y, text, ans_len=False, background=None):
    input_text = []
    line_length = 0
    insert_text(board, x, y, text, background)
    print_board(board)
    line_length += len(str(text))
    key = None
    if background is None:
        prefix = ''
        suffix = ''
    else:
        prefix = background[:10]
        suffix = background[-4:]
    while key != '\r' or len(input_text) == ans_len:
        key = getch()
        if key == '\r':
            pass
        elif key == '\x7f':  # backspace ramoves last char
            board[y][x + line_length - 1] = prefix + ' ' + suffix
            line_length -= 1
            del input_text[-1]
        else:
            board[y][x + line_length] = prefix + key + suffix
            line_length += 1
            input_text.append(key)
        print_board(board)
    return ''.join(input_text)


def load_info(info_file):
    with open('texts/' + info_file + '.txt', 'r', newline='\n') as text_file:
        text_file = text_file.readlines()
        dynamite_info = [line[:-1] for line in text_file[18:26]]
        metal_detector_info = [line[:-1] for line in text_file[28:34]]
        chemical_suit_info = [line[:-1] for line in text_file[36:43]]
        armour_info = [line[:-1] for line in text_file[45:49]]
        flag_info = [line[:-1] for line in text_file[51:54]]
        vaccine_info = [line[:-1] for line in text_file[56:59]]
    return {'dynamite': dynamite_info, 'metal_detector': metal_detector_info, 'chemical_suit': chemical_suit_info,
            'armour': armour_info, 'flag': flag_info, 'vaccine': vaccine_info}
