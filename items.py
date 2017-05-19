import random
from maps_creator import *
from hero import *
from text_in_out import *


class Item:

    EQUIPMENT = ['dynamite', 'metal_detector', 'chemical_suit', 'armour', 'flag', 'vaccine']
    EQUIPMENT_WEIGHT = {'dynamite': 2, 'metal_detector': 4, 'chemical_suit': 8,
                        'armour': 5, 'flag': 1, 'vaccine': 2}

    info = load_info('equipment')
    maps_instantions = load_maps('maps')

    def choose_random_map(self):
        self.place = Item.maps_instantions[random.choice(list(Item.maps_instantions))]

    def set_position(self):
        ready = False
        while not ready:
            start = (random.randint(2, (len(self.place.board[0]) - 4)),
                     random.randint(2, (len(self.place.board) - 4)))
            self.position = calc_neighbours(start, distance=self.large)
            if all([self.place.board[y][x] == ' ' for x, y in self.position]):
                ready = True

#        elif self.item_type = 'bomb':
#            self.char = COLOURS['F']

    def put_on_board(self):
        self.place.objects.append(self)
        if self.large > 0:
            for x, y in self.position:
                self.place.board[y][x] = self.char
        else:
            x, y = self.position
            self.place.board[y][x] = self.char

    def hide_on_board(self):
        if self.large > 0:
            for x, y in self.position:
                self.place.board[y][x] = ' '
        else:
            self.place.board[self.position[1]][self.position[0]] = ' '


class Box(Item):
    """docstring for Item ."""

    def __init__(self, content):
        self.type = 'box'
        self.char = Maps.COLOURS['T']
        self.large = 1
        self.choose_random_map()
        self.set_position()
        self.opened = False
        self.content = Equipment(content)
        self.put_on_board()

    def open(self):
        if not self.opened:
            for x, y in self.position:
                self.place.board[y][x] = ' '
            self.content.place = self.place
            self.content.position = self.position[1]
            self.place.objects.remove(self)
            self.content.put_on_board()
            self.opened = True


class Bomb(Item):

    BOMB_DISARMING_VALUES = {
        'A': (3, True, False),
        'B': (4, False, True),
        'C': (5, False, False)
    }

    POINTS_FOR_DISARMING = {'A': 10, 'B': 20, 'C': 30, 'N': 100}

    def __init__(self, bomb_type):
        self.type = 'bomb'
        self.bomb_type = bomb_type
        self.attempts = 10
        self.is_armed = True
        self.generate_disarm_code(*Bomb.BOMB_DISARMING_VALUES[self.bomb_type])
        self.char = Maps.COLOURS['F']
        self.large = 2
        self.choose_random_map()
        self.set_position()
        self.put_on_board()

    def generate_disarm_code(self, number_length=3, is_binary=False, is_even=False):
        digits = 9
        self.disarm_code = []
        if is_binary:
            digits = 1
        even_numbers = [0, 2, 4, 6, 8]
        while len(self.disarm_code) != number_length:
            if is_even:
                num = random.choice(even_numbers)
                if num not in self.disarm_code:
                    self.disarm_code.append(str(num))
            else:
                num = random.randint(0, digits)
                if num not in self.disarm_code:
                    self.disarm_code.append(str(num))

    def guess_number(self, player):
        guess_result = []
        guess_number = []
        is_playing = True
        while self.attempts and is_playing:
            pop_up(self.place.board, ['You got {} attempts'.format(self.attempts), ' ', ' '.join(guess_number), ' '.join(guess_result)], auto_hide=2)
            correct_input = False
            while not correct_input:
                guess_number = pop_up(self.place.board, ["pick {} digit number: ".format(len(self.disarm_code))], ask=True, ans_len=len(self.disarm_code))
                print(guess_number)
                if guess_number.isdigit():
                    guess_number = list(guess_number)
                    correct_input = True
                elif guess_number == '\r':
                    is_playing = False
                    break
                else:
                    pop_up(self.place.board, ["It is not an integer!"], auto_hide=2)
            guess_result = []
            for i, elem in enumerate(guess_number):
                if elem in self.disarm_code:
                    if elem == self.disarm_code[i]:
                        guess_result.append('H')
                    else:
                        guess_result.append('W')
                else:
                    guess_result.append('C')

            if all([i == 'h' for i in guess_result]):
                result_print = ['You guessed the number']
                self.is_armed = False
                is_playing = False
                player.exp += Bomb.POINTS_FOR_DISARMING[self.bomb_type]
                break
            self.attempts -= 1
        if not self.attempts:
            pop_up(self.place.board, ['You lose'], auto_hide=2)
            is_playing = False
            self.explode(player)
        else:
            pop_up(self.place.board, ['You abort disarming. Remaining attempts: {}'.format(self.attempts)], auto_hide=2)

    def explode(self, player):
        print(self.position[0])
        sleep(3)
        if self.bomb_type == 'A':
            player.make_boom(self.position[12], power=10)
        elif self.bomb_type == 'B':
            player.make_boom(self.position[12], power=10, is_deadly=False)
            for x, y in calc_neighbours(self.position[0], distance=10):
                self.place.board[y][x] = '☣'
        elif self.bomb_type == 'C':
            player.make_boom(self.position[12], power=15, is_deadly=False)
            for x, y in calc_neighbours(self.position[0], distance=15):
                self.place.board[y][x] = '~'
        elif self.bomb_type == 'N':
            player.make_boom(self.position[12], power=10, is_deadly=False)
            pop_up(self.place.board, ['GAME OVER'], auto_hide=2)


class Equipment(Item):

    def __init__(self, content):
        self.type = content
        self.large = 0
        self.set_char_look()
        self.info
        self.info = Item.info[self.type]

    def set_char_look(self):
        if self.type == 'dynamite':
            self.char = '⌫'
        elif self.type == 'metal_detector':
            self.char = '♩'
        elif self.type == 'chemical_suit':
            self.char = 'C'
        elif self.type == 'armour':
            self.char = 'A'
        elif self.type == 'flag':
            self.char = '⚑'
        elif self.type == 'vaccine':
            self.char = '💉'
