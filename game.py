import os
import sys
import random
import time
from maps_creator import *
from hero import *
from text_in_out import *
from items import *


def action(player, key):
    game_on = True
    if key == '1':
        player.browse_backpack()
    elif key == '2':
        pass  # INSTRUCTIONS
    elif key == '3':
        pass  # CONTROLS
    elif key == '4':
        pop_up(player.place.board, ['You have exited a game'], auto_hide=1)
        game_on = False
    elif key == 'e':
        player.react_with_object()
    elif key == 'b':
        player.detonate_dynamite()
    else:
        player.move(key)
    return game_on


def end_game(board):
    pop_up(board, ['HIGHSCORES'], auto_hide=2)
    os.system('clear')


def main():
    player = Hero()
    game_on = True
    player.insert_on_board()
    while player.alive and game_on:
        print_board(player.place.board, player)
        key = getch().lower()
        game_on = action(player, key)
        player.insert_on_board()
    end_game(player.place.board)


if __name__ == '__main__':
    main()
