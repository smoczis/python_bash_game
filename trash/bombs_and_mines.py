import random

nuke_bomb = {'exp_require': 10000,
             'wisdom_required': 5 + random.randint(1, 10),
             'mental_strength_required': 10
             'code_required': 'hero goes secret code',
             'count_down': 60}

hidden_mine = {}
hidden_mine2 = {}
hidden_mine3 = {}
bomb1 = {}
bomb2 = {}
bomb3 = {}


class Bomb():

    def __init__(self, bomb_type, is_disarmed=False):
        self.place = random.choice(Item.maps_instantions)
        self.set_position()
        self.insert()
        self.attempts = 10
        self.bomb_type = bomb_type
        self.is_armed = is_armed
        self.disarm_code = []
        self.generate_disarm_code(*BOMB_DISARMING_VALUES[self.bomb_type])

'''
    def set_position(self, range):
        ready = False
        while not ready:
            start = (random.randint(2, (len(self.place.board[0]) - 4)),
                     random.randint(2, (len(self.place.board) - 4)))
            self.position = []
            for delta_y in range(3):
                for delta_x in range(3):
                    if self.place.board[start[1] + delta_y][start[0] + delta_x] == ' ':
                        self.position.append((start[0] + delta_x, start[1] + delta_y))
                        ready = True
                    else:
                        ready = False

    def insert(self, bomb_type):
        # insert a bomb as a square in available position
        for x, y in self.position:
            self.place.board[y][x] = COLOURS['F']
        # in the center of square replaces one char with a letter corresponding to bomb type
        self.place.board[self.position[4][0]][self.position[4][1]] = self.bomb_type
'''

    def generate_disarm_code(self, number_length=3, is_binary=False, is_even=False):
        digits = 9
        if is_binary:
            digits = 1
        even_numbers = [0, 2, 4, 6, 8]
        while len(self.disarm_code) != number_length:
            if is_even:
                num = choice(even_numbers)
                if num not in self.disarm_code:
                    self.disarm_code.append(str(num))
            else:
                num = randint(0, digits)
                if num not in self.disarm_code:
                    self.disarm_code.append(str(num))

    def guess_number(self):
        guess_result = []
        guess_number = []
        is_playing = True
        while self.attempts and is_playing:
            pop_up(self.place.board, ['You got {} attempts'.format(self.attempts), ' ', ' '.join(guess_number), ' '.join(guess_result)])
            correct_input = False
            while not correct_input:
                guess_number = pop_up(self.place.board, ["pick {} digit number: ".format(len(self.disarm_code))], ask=True, ans_len=len(self.disarm_code))
                if guess_number.isdigit():
                    guess_number = list(guess_number)
                    correct_input = True
                elif guess_number == ' ':
                    is_playing = False
                else:
                    pop_up(self.place.board, ["It is not an integer!"], auto_hide=2)

            # print ("You got {} attempts".format(attempts))
            # print (guess_number)
            guess_result = []
            for i, elem in enumerate(guess_number):
                if elem in self.disarm_code:
                    if elem == self.disarm_code[i]:
                        guess_result.append('h')
                    else:
                        guess_result.append('w')
                else:
                    guess_result.append('c')

            if all([i == 'h' for i in guess_result]):
                result_print = ['You guessed the number']
                self.is_disarmed = True
                is_playing = False
                break
            self.attempts -= 1
        if not self.attempts:
            result_print = ['You lose']
            is_playing = False
        else:
            result_print = ['You abort disarming. Remaining attempts: {}'.format(self.attempts)]
        pop_up(self.place.board, result_print, auto_hide=2)


    def disarm_bomb(self, board, bomb_type, is_disarmed):
        is_disarmed = hot_cold(board, *BOMB_DISARMING_VALUES[bomb_type])
        if not is_disarmed:
            pass
            # boom(actual, x, y)
