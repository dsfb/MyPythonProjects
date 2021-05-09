# Write your code here

from collections import defaultdict
from datetime import datetime

import math
import random

random.seed(int(datetime.now().timestamp()))


def get_piece_counting(piece_list, counter):
    flat_list = [item for sublist in piece_list for item in sublist]
    for i in range(7):
        counter[i] += flat_list.count(i)
    return counter


def has_double(dominoes):
    candidate = None
    for domino in dominoes:
        if domino[0] == domino[1]:
            if candidate is None or domino[0] > candidate[0]:
                candidate = list(domino)

    return candidate is not None, candidate


class Game:
    def __init__(self):
        self.full_dominoes = []
        self.stock_pieces = []
        self.computer_pieces = []
        self.player_pieces = []
        self.domino_snake = []
        self.status = ''
        self.turn = None # 0, for player, and 1, for computer.
        self.choice = None
        self.computer_choice = None
        self.create_sets()
        self.process_starting()
        self.process_game()

    def print_interface(self):
        print('======================================================================')
        print(f'Stock size: {len(self.stock_pieces)}')
        print(f'Computer pieces: {len(self.computer_pieces)}')
        print()
        self.show_domino_snake()
        print()
        print('Your pieces:')
        for i in range(len(self.player_pieces)):
            print(f'{i + 1}:{self.player_pieces[i]}')
        print()
        if self.status == "computer":
            print("Status: Computer is about to make a move. Press Enter to continue...")
        elif self.status == "player":
            print("Status: It's your turn to make a move. Enter your command.")

    def process_input(self):
        if self.turn == 1:
            input()
            self.make_computer_move()
        elif self.turn == 0:
            self.process_player_move()

    def make_computer_move(self):
        counter = defaultdict(int)
        counter = get_piece_counting(self.computer_pieces, counter)
        counter = get_piece_counting(self.domino_snake, counter)
        if self.computer_pieces:
            computer_pieces_shadow = self.computer_pieces[:]
            while computer_pieces_shadow:
                summer = dict()
                for index, elem in enumerate(computer_pieces_shadow):
	                summer[index] = sum([counter[single] for single in elem])
                data = list(summer.values())
                piece = computer_pieces_shadow[data.index(max(data))]
                if piece.count(self.domino_snake[0][0]):
                    if piece[0] == self.domino_snake[0][0]:
                        self.put_piece_domino_snake(self.computer_pieces.pop(data.index(max(data)))[::-1], True)
                    elif piece[1] == self.domino_snake[0][0]:
                        self.put_piece_domino_snake(self.computer_pieces.pop(data.index(max(data))), True)
                    break
                elif piece.count(self.domino_snake[-1][-1]):
                    if piece[0] == self.domino_snake[-1][-1]:
                        self.put_piece_domino_snake(self.computer_pieces.pop(data.index(max(data))), False)
                    elif piece[1] == self.domino_snake[-1][-1]:
                        self.put_piece_domino_snake(self.computer_pieces.pop(data.index(max(data)))[::-1], False)
                    break
                else:
                    computer_pieces_shadow.pop(data.index(max(data)))

            if not computer_pieces_shadow:
                self.computer_pieces.append(self.stock_pieces.pop(0))
                

    def put_piece_domino_snake(self, piece, left_side):
        if left_side:
            self.domino_snake.insert(0, piece)
        else:
            self.domino_snake.append(piece)

    def show_domino_snake(self):
        if len(self.domino_snake) > 6:
            snake = self.domino_snake
            print(f'{snake[0]}{snake[1]}{snake[2]}...{snake[-3]}{snake[-2]}{snake[-1]}')
        else:
            string = ''
            for piece in self.domino_snake:
	            string += str(piece)
            print(string)

    def process_player_move(self):
        while len(self.player_pieces):
            try:
                self.choice = int(input())
                side = self.choice < 0
                self.choice = int(math.fabs(self.choice))
                if self.choice == 0:
                    if len(self.stock_pieces):
                        self.player_pieces.append(self.stock_pieces.pop(self.choice))
                        return
                    else:
                        print('Illegal move. Please try again.')
                        continue
                elif self.choice < 1 or self.choice > len(self.player_pieces):
                    raise ValueError()
                else:
                    piece = self.player_pieces[self.choice - 1]
                    if self.domino_snake[0][0] not in piece and self.domino_snake[-1][-1] not in piece:
                        print('Illegal move. Please try again.')
                        continue
                break
            except ValueError:
                print('Invalid input. Please try again.')

        piece = self.player_pieces.pop(self.choice - 1)
        if self.domino_snake[0][0] in piece:
            side = True
            if piece[0] == self.domino_snake[0][0]:
                self.put_piece_domino_snake(piece[::-1], side)
            else:
                self.put_piece_domino_snake(piece, side)
        elif self.domino_snake[-1][-1] in piece:
            side = False
            if piece[0] == self.domino_snake[-1][-1]:
                self.put_piece_domino_snake(piece, side)
            else:
                self.put_piece_domino_snake(piece[::-1], side)

    def process_game(self):
        while len(self.computer_pieces) and len(self.player_pieces):
            self.print_interface()
            self.process_input()
            self.process_turn()
        
        self.print_interface()
        
        if not self.player_pieces:
            print('Status: The game is over. You won!')
        elif not self.computer_pieces:
            print('Status: The game is over. The computer won!')

    def process_turn(self):
        self.turn += 1
        self.turn %= 2
        if self.turn == 1:
           self.status = "computer" 
        elif self.turn == 0:
            self.status = "player"

    def create_sets(self):
        for i in range(0, 7):
            for j in range(i, 7):
                self.full_dominoes.append([i, j])

        for i in range(14):
            self.stock_pieces.append(self.full_dominoes.pop(random.randrange(0, 28 - i)))

        for i in range(7):
            self.computer_pieces.append(self.full_dominoes.pop(random.randrange(0, 14 - i)))

        for i in range(7):
            self.player_pieces.append(self.full_dominoes.pop(random.randrange(0, 7 - i)))

    def process_starting(self):
        while True:
            double_computer = has_double(self.computer_pieces)
            double_player = has_double(self.player_pieces)
            if double_computer[0] and double_player[0]:
                if double_computer[1][0] > double_player[1][0]:
                    self.status = 'player'
                    starting_piece = double_computer[1]
                    self.computer_pieces.remove(starting_piece)
                    break
                elif double_computer[1][0] < double_player[1][0]:
                    self.status = 'computer'
                    starting_piece = double_player[1]
                    self.player_pieces.remove(starting_piece)
                    break
            elif double_computer[0]:
                self.status = 'player'
                starting_piece = double_computer[1]
                self.computer_pieces.remove(starting_piece)
                break
            elif double_player[0]:
                self.status = 'computer'
                starting_piece = double_player[1]
                self.player_pieces.remove(starting_piece)
                break
            else:
                self.create_sets()

        self.domino_snake.append(starting_piece)

        if self.status == "computer":
            self.turn = 1
        elif self.status == "player":
            self.turn = 0


game = Game()

