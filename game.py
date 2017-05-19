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


def end_game(player, start_time):
    game_time = round(time.time() - start_time)
    final_score = 1000 - game_time + player.exp
    saved_scores = open('texts/scores.txt').readlines()
    new_score = "{} - {} - {}\n".format(final_score, game_time, player.name)
    if not saved_scores:
        saved_scores.append(new_score)
    else:
        i = 0
        new_index = len(saved_scores)
        for line in saved_scores:
            line_elem = line.strip()
            line_elem = line_elem.split(' - ')
            if final_score >= int(line_elem[0]):
                new_index = i
                break
            i += 1
        saved_scores.insert(new_index, new_score)
    with open("texts/scores.txt", 'w') as fw:
        iterator = 0
        while iterator < 10 and iterator < len(saved_scores):
            fw.write(saved_scores[iterator])
            iterator += 1
    score_list = open('texts/scores.txt').readlines()
    new_list = []
    for score in score_list:
        score = score[:-1]
        new_list.append(score)
    new_list.insert(0, 'HIGHSCORES')
    new_list.insert(1, 'SCORE - GAME TIME - NAME')
    pop_up(player.place.board, new_list, auto_hide=4)
    os.system('clear')


def show_intro(player):
    intro_screens = [files for files in os.listdir('texts') if files.endswith('screen.txt')]
    intro_screens = sorted(intro_screens)
    for screen in intro_screens:
        board_to_print = []
        file_path = 'texts/' + screen
        with open(file_path, 'r', newline='\n') as fo:
            for line in fo:
                board_to_print.append(line[:-1])
        pop_up(player.place.board, board_to_print)


def main():
    player = Hero()
    show_intro(player)
    player.get_player_name()
    player.choose_equipment()
    game_on = True
    start_time = time.time()
    player.insert_on_board()
    while player.alive and game_on:
        print_board(player.place.board, player)
        key = getch().lower()
        game_on = action(player, key)
        player.insert_on_board()
    end_game(player, start_time)


if __name__ == '__main__':
    main()
