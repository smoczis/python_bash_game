"""
start menue
win/lose screen
map!!!
hot_cold with pop_up
"""
from random import randint, choice
from text_in_out import *


def hot_cold(board, number_length, attempts, is_binary=False, is_even=False):
    number = generate_number(number_length, is_binary, is_even)
    win = guess_number(board, number, attempts, number_length)
    return win


def generate_number(number_length=3, is_binary=False, is_even=False):
    generated_number = []
    digits = 9
    if is_binary:
        digits = 1
    even_numbers = [0, 2, 4, 6, 8]
    while len(generated_number) != number_length:
        if is_even:
            num = choice(even_numbers)
            if num not in generated_number:
                generated_number.append(str(num))
        else:
            num = randint(0, digits)
            if num not in generated_number:
                generated_number.append(str(num))
    return generated_number


def guess_number(board, generated_number, attempts, number_length=3):
    guess_result = []
    guess_number = []
    while attempts:
        pop_up_list = ['You got {} attempts'.format(attempts), ' ', ' '.join(guess_number), ' '.join(guess_result)]
        pop_up(board, pop_up_list)
        correct_input = False
        while not correct_input:
            guess_number = pop_up(board, ["pick {} digit number: ".format(number_length)], ask=True, ans_len=number_length)
            if guess_number.isdigit():
                guess_number = list(guess_number)
                correct_input = True
            else:
                pop_up(board, ["It is not an integer!"], auto_hide=2)

        # print ("You got {} attempts".format(attempts))
        # print (guess_number)
        guess_result = []
        for i, elem in enumerate(guess_number):
            if elem in generated_number:
                if elem == generated_number[i]:
                    guess_result.append('h')
                else:
                    guess_result.append('w')
            else:
                guess_result.append('c')

        if all([i == 'h' for i in guess_result]):
            result_print = ['You guessed the number']
            win = True
            break
        attempts -= 1
    else:
        result_print = ['You lose']
        win = False
    pop_up(board, result_print, auto_hide=2)
    return win
