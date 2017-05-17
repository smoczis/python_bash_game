import os
import sys
import random
import time
from maps_creator import *
from hero import *
from text_in_out import *
from items import *


def action(player):
    game_on = True
    key = getch().lower()
    if key == '1':
        browse_backpack(player)
    elif key == '2':
        pass  # INSTRUCTIONS
    elif key == '3'":
        pass  # CONTROLS
    elif key == '4':
        pop_up(player.place.board, ['You have exited a game'], auto_hide=1)
        game_on = False
    elif key == 'e':
        react_with_object()
    return game_on


def end_game(board):
    pop_up(board, ['HIGHSCORES'], auto_hide=2)
    os.system('clear')


def main():
    player = Hero(load_maps('maps'))
    game_on = True
    while player.alive and game_on:
        player.insert_on_board
        print_board(player.place.board, player)
        key = getch().lower()
        player.move(key)
        game_on = action(key)
    end_game(player.place.board)


if __name__ == '__main__':
    main()
