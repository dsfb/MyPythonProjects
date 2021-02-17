# Write your code here
import random
import sys


random.seed(0)

print("H A N G M A N")


def game():
    tries = 8

    print()
    list_answer = ['python', 'java', 'kotlin', 'javascript']
    answer = list_answer[random.randint(0, len(list_answer) - 1)]

    acceptable = 'abcdefghijklmnopqrstuvxywz'

    guessed = []
    guess = ['-', ] * len(answer)
    current = ''
    while tries and ''.join(guess) != answer:
        print(''.join(guess))
        current = input('Input a letter:')
        if len(current) != 1:
            print("You should input a single letter")
            print()
            continue
        elif current.isupper() or acceptable.find(current) == -1:
            print('Please enter a lowercase English letter')
            print()
            continue
        elif guessed.count(current) == 0:
            guessed.append(current)
        else:
            print("You've already guessed this letter")
            print()
            continue

        try:
            index = answer.index(current)
            if guess[index] == '-':
                guess[index] = current
                while answer.rfind(current) > answer.find(current, index):
                    index += 1
                    index = answer.index(current, index)
                    guess[index] = current
            elif guess[index] == answer[index]:
                print('No improvements')
                tries -= 1
        except ValueError:
            print("That letter doesn't appear in the word")
            tries -= 1
        finally:
            if tries:
                print()

    if ''.join(guess) == answer:
        print(answer)
        print("You guessed the word!")
        print("You survived!")
    else:
        print("You lost!")


while True:
    choice = input('Type "play" to play the game, "exit" to quit:')
    if choice == 'play':        
        game()
    elif choice == 'exit':
        sys.exit()
