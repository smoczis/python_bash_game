import sys
import tty
import termios
from maps_creator import print_board, COLOURS
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
