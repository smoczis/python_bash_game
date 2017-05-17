import os
from re import match
from time import sleep
from text_in_out import *


def choose_eq(actual, backpack_capicity):
    EQUIPMENT = ['dynamite', 'metal_detector', 'chemical_suit', 'armour', 'flag', 'vaccine']
    EQUIPMENT_WEIGHT = {'dynamite': 2, 'metal_detector': 4, 'chemical_suit': 8, 'armour': 5, 'flag': 1, 'vaccine': 2}
    with open('texts/equipment.txt', 'r', newline='\n') as text_file:
        text_file = text_file.readlines()
        equipment_intro = [line[:-1] for line in text_file[:6]]
        equipment_menu = [line[:-1] for line in text_file[8:16]]
        dynamite_info = [line[:-1] for line in text_file[18:26]]
        metal_detector_info = [line[:-1] for line in text_file[28:34]]
        chemical_suit_info = [line[:-1] for line in text_file[36:43]]
        armour_info = [line[:-1] for line in text_file[45:49]]
        flag_info = [line[:-1] for line in text_file[51:54]]
        vaccine_info = [line[:-1] for line in text_file[56:59]]
    for_more_info = {'q': dynamite_info, 'w': metal_detector_info,
                     'e': chemical_suit_info, 'r': armour_info,
                     't': flag_info, 'y': vaccine_info}
    pop_up(actual.board, equipment_intro)
    backpack = []
    backpack_space = backpack_capicity
    ready = False
    while not ready:
        choose = pop_up(actual.board, equipment_menu +
                                      [' ', "You've taken: ", ' ', *backpack, ' ',
                                      'You still can pack ' + str(backpack_space) + ' kg'])
        if choose.lower() in for_more_info:
            pop_up(actual.board, for_more_info[choose.lower()])
        elif choose in ['1', '2', '3', '4', '5', '6']:
            index = int(choose) - 1
            if EQUIPMENT[index] in backpack:
                backpack.remove(EQUIPMENT[index])
                backpack_space += EQUIPMENT_WEIGHT[EQUIPMENT[index]]
            elif EQUIPMENT_WEIGHT[EQUIPMENT[index]] <= backpack_space:
                backpack.append(EQUIPMENT[index])
                backpack_space -= EQUIPMENT_WEIGHT[EQUIPMENT[index]]
            else:
                pop_up(actual.board, ["You don't have so much space for that item!"], auto_hide=1)
        elif choose == ' ':
            ready = True
        elif choose == '.':
            raise KeyboardInterupt
        else:
            pop_up(actual.board, ['Wrong choose!'], auto_hide=1)
    return backpack
