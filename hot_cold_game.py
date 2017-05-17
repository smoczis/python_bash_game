"""
start menue
win/lose screen
map!!!
hot_cold with pop_up
"""
from random import randint, choice


def generate_number(number_length=3, is_binary=False, is_even=False):
    random_number = []
    digits = 9
    if is_binary:
        digits = 1
    even_numbers = [0, 2, 4, 6, 8]
    while len(random_number) != number_length:
        if is_even:
            num = choice(even_numbers)
            if num not in random_number:
                random_number.append(str(num))
        else:
            num = randint(0, digits)
            if num not in random_number:
                random_number.append(str(num))
    return random_number


def guessing_number(random_number, attempts, number_length=3):
    printing_result = []
    while attempts:
        pop_up_list = ['You got {} attempts'.format(attempts), '\n', *printing_result]
        print (*pop_up_list)
        guess_number = input("pick {} digit number: ".format(number_length))

        while not guess_number.isdigit() or len(guess_number) != number_length:
            guess_number = input("It is not an integer!")

        # print ("You got {} attempts".format(attempts))
        guess_number = list(guess_number)
        # print (guess_number)
        printing_result = []
        for i, elem in enumerate(guess_number):
            if elem in random_number:
                if elem == random_number[i]:
                    printing_result.insert(0, 'hot')
                else:
                    printing_result.append('warm')

        if not printing_result:
            printing_result = ['cold']

        if all([i == 'hot' for i in printing_result]) and len(printing_result) == number_length:
            pop_up_list = ['You guessed the number']
            break
        attempts -= 1
    else:
        pop_up_list = ['You lose']
    return pop_up_list


def main():
    number = generate_number(number_length=5)
    print (number)
    print (guessing_number(number, 10, number_length=5))


if __name__ == "__main__":
    main()
