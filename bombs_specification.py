import random


nuke_bomb = { 'exp_require': 10000,
              'wisdom_required': 30,
              'mental_strength_required':  5 + random.randint(1,10),
              'code_required': 'hero goes secret code',
              'count_down': 60 }

hidden_mine = {'wisdom_required': 2}
hidden_mine2 = {'wisdom_required': 4}
hidden_mine3 = {'wisdom_required': 6}
bomb1 = {}
bomb2 = {}
bomb3 = {}


def put_mines(quantity):
    """randomly selecting positions of given quantity of mines. returns a list of tuples (x, y)"""
    miles = []
    global board
    while len(mines) < quantity:
        y = random.randint(0, len(board)-1)
        x = random.randint(0, len(board[0])-1)
        if board[y][x] == ' ':
            mines.append((x, y))
    return mines


def hide_mines():
    """hiding all mines, that were printed before by show_neighbours()"""
    global mines
    global board
    for line_i in range(len(board)):
        for char_i in range(len(board[line_i])):
            if board[line_i][char_i] == 'X':
                board[line_i][char_i] = ' '
    return board


def boom(x, y):
    """this happening when player steps on mine or bomb explodes"""
    global board
    board_backup = board