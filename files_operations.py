from text_in_out import *
from maps_creator import *
from hero import *
import csv


def starter():
    global maps_instantions
    action = input('N for new game, L to load:')
    if action.upper() == 'N':
        actual = maps_instantions[0]
        hero = create_hero()
        actual.player_position = 28, 5
    elif action.upper() == 'L':
        game_file = input('Enter file name:')
        game = load(game_file)
        print(game[3])
        actual = game[3]
        hero = game[2]
        for m in maps_instantions:
            if m == actual:
                actual.player_position = m.player_position
    return actual, hero, actual.player_position


def save(actual, hero):
    data = collect_data(actual, hero)
    with open('save/' + data[0] + '.csv', 'w') as save:
        writer = csv.writer(save, delimiter=',')
        writer.writerow([x for x in data])
    print_text(actual.board, 50, 20, "SAVED")


def load(game_file):
    global maps_instantions
    with open('save/' + game_file + '.csv', 'r') as save:
        reader = csv.reader(save, delimiter=',')
        l = []
        for line in reader:
            l.append(line)
        load = l[0]
        print(load[3][0][0])
        file_name = load[0]
        player_name = load[1]
        for i in range(0, len(load[2]), 2):
            if load[2][i+1] == '[]':
                hero[load[2][i]] = []
            elif load[2][i+1] == 'True':
                hero[load[2][i]] = True
            elif load[2][i+1] == 'False':
                hero[load[2][i]] = False
            else:
                hero[load[2][i]] = int(load[2][i+1])
        for i, m in enumerate(maps_instantions):
            m.board = load[3][i][0]
            m.mines = load[3][i][1]
            m.player_objects = load[3][i][2]
            m.player_position = load[3][i][3]
        actual = maps_instantions[int(load[4])]
    return file_name, player_name, hero, actual


def collect_data(actual, hero):
    player_name =pop_up(['Enter player name:'], ask=True)
    file_name = pop_up(['Enter file name:'], ask=True)
    data = [file_name, player_name]
    global maps_instantions
    print(hero)
    actual_index = None
    player = []
    getch()
    for item in hero:
        player.append(item)
        player.append(hero[item])
    data.append(player)
    board = [(m.board, m.mines, m.player_objects, m.player_position) for m in maps_instantions]
    actual_index = maps_instantions.index(actual)
    data.append(board)
    data.append(actual_index)
    print(data)
    return data
