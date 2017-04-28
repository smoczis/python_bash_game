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
board = []
mines = []




def boom(x, y):
    """this happening when player steps on mine or bomb explodes"""
    global board
    board_backup = board
