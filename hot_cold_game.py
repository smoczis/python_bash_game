"""
develop hotcold game using popup window
start menue
win/lose screen
chest on classes
map!!!

"""
from random import randint, choice


def generate_number(binary=False, even=False):
    random_number = []
    digits = 9
    if binary:
        digits = 1
    even_nums = [0, 2, 4, 6, 8]
    while len(random_number) != 3:
        if even:
            num = choice(even_nums)
            if num not in random_number:
                random_number.append(str(num))
        else:
            num = randint(0, digits)
            if num not in random_number:
                random_number.append(str(num))
    return random_number
# random_number = ''.join(random_number)


def guessing_number(random_number, attempts):
    while attempts:
        printing_result = []
        pop_up_list = ['You got {} attempts'.format(attempts), '\n', *printing_result]
        print (*pop_up_list)
        guess_number = input("pick 3 digit number: ")

        while not guess_number.isdigit() or len(guess_number) != 3:
            guess_number = input("It is not an integer!")

        # print ("You got {} attempts".format(attempts))
        guess_number = list(guess_number)
        # print (guess_number)


        for i, elem in enumerate(guess_number):
            if elem in random_number:
                if elem == random_number[i]:
                    printing_result.insert(0, 'hot')
                else:
                    printing_result.append('warm')

        if not printing_result:
            print ("cold")

        print (*printing_result)
        if all([i == 'hot' for i in printing_result]) and len(printing_result) == 3:
            print ('cool')
            break
        attempts -= 1
    else:
        pop_up_list = ['You lose']
    return pop_up_list
    '''
     goal = "".join(printing_result)
    if goal == "hothothot":
        print ("Cool")
        break
        '''


def main():
    number = generate_number(even=True)
    print (guessing_number(number, 10))


if __name__ == "__main__":
    main()
