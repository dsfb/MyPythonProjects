# Write your code here
import random

random.seed(0)


def computer_wins(user, computer):
    computer_winning_cases = {
        'water': ['scissors', 'fire', 'rock', 'hun', 'lightning', 'devil', 'dragon'],
        'dragon': ['snake', 'scissors', 'fire', 'rock', 'gun', 'lightning', 'devil'],
        'devil': ['tree', 'human', 'snake', 'scissors', 'fire', 'rock', 'gun'],
        'gun': ['wolf', 'tree', 'human', 'snake', 'scissors', 'fire', 'rock'],
        'rock': ['sponge', 'wolf', 'tree', 'human', 'snake', 'scissors', 'fire'],
        'fire': ['paper', 'sponge', 'wolf', 'tree', 'human', 'snake', 'scissors'],
        'scissors': ['air', 'paper', 'sponge', 'wolf', 'tree', 'human', 'snake'],
        'snake': ['water', 'air', 'paper', 'sponge', 'wolf', 'tree', 'human'],
        'human': ['dragon', 'water', 'air', 'paper', 'sponge', 'wolf', 'tree'],
        'tree': ['devil', 'dragon', 'water', 'air', 'paper', 'sponge', 'wolf'],
        'wolf': ['lightning', 'devil', 'dragon', 'water', 'air', 'paper', 'sponge'],
        'sponge': ['gun', 'lightning', 'devil', 'dragon', 'water', 'air', 'paper'],
        'paper': ['rock', 'gun', 'lightning', 'devil', 'dragon', 'water', 'air'],
        'air': ['fire', 'rock', 'gun', 'lightning', 'devil', 'dragon', 'water'],
        'lightning': ['tree', 'human', 'snake', 'scissors', 'fire', 'rock', 'gun']
    }

    return user in computer_winning_cases[computer]


name = input('Enter your name:')
print(f'Hello, {name}')

option_input = input()
if not option_input:
    options = ['scissors', 'paper', 'rock']
else:
    options = option_input.split(',')

print("Okay, let's start")

players = {}

rating_file = open('rating.txt', 'r')
lines = rating_file.readlines()
for line in lines:
    tokens = line.rstrip().split(' ')
    players[tokens[0]] = int(tokens[1])

if name not in players:
    players[name] = 0

user = input()

while user != '!exit':
    if user == '!rating':
        print(f'Your rating: {players[name]}')
        user = input()
        continue
    elif user not in options:
        print('Invalid input')
        user = input()
        continue

    choice = random.randint(0, len(options) - 1)
    computer = options[choice]

    user_lose = f'Sorry, but the computer chose {computer}'
    user_draw = f'There is a draw ({computer})'
    user_win = f'Well done. The computer chose {computer} and failed'

    ending = {0: user_lose, 1: user_draw, 2: user_win}
    result = 2

    if computer == user:
        result = 1
        players[name] = players[name] + 50
    elif computer_wins(user, computer):
        result = 0
    else:
        players[name] = players[name] + 100

    print(ending[result])
    user = input()
else:
    print('Bye!')

with open('rating.txt', 'w') as out_file:
    for name in players:
        out_file.write(name + ' ' + str(players[name]))
