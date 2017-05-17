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


def pop_up(board, text_lines, auto_hide=0, ask=False, ans_len=False, colour=COLOURS['C']):
    global COLOURS
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
        print_text(board_copy, x_start + 3, 7 + i, item, background=colour)
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


def print_text(board, x, y, text, background=None):
    global COLOURS
    if background is None:
        prefix = ''
        suffix = ''
    else:
        prefix = background[:10]
        suffix = background[-4:]
    for i, char in enumerate(str(text)):
        board[y][x + i] = prefix + char + suffix
    return board


def get_input(board, x, y, text, ans_len=False, background=None):
    global COLOURS
    input_text = []
    line_length = 0
    print_text(board, x, y, text, background)
    print_board(board)
    line_length += len(str(text))
    key = None
    if background is None:
        prefix = ''
        suffix = ''
    else:
        prefix = background[:10]
        suffix = background[-4:]
    if not ans_len:
        while key != ' ':
            key = getch()
            if key != ' ':
                board[y][x + line_length] = prefix + key + suffix
                line_length += 1
                input_text.append(key)
            print_board(board)
    else:
        for i in range(ans_len):
            key = getch()
            if key != ' ':
                board[y][x + line_length] = prefix + key + suffix
                line_length += 1
                input_text.append(key)
            print_board(board)
    return ''.join(input_text)
