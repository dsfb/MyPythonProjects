# write your code here

import random


while True:
    try:
        print('Which level do you want? Enter a number:')
        print('1 - simple operations with numbers 2-9')
        print('2 - integral squares of 11-29')
        level = int(input())
        if level not in (1, 2):
            raise ValueError()
        break
    except ValueError:
        print('Incorrect format.')

marks = 0
if level == 1:
    for _ in range(5):
        first_number = random.randint(2, 9)
        second_number = random.randint(2, 9)
        operation_type = random.randint(1, 3)

        if operation_type == 1:  # multiplication
            operation = str(first_number) + ' * ' + str(second_number)
        elif operation_type == 2:  # addition
            operation = str(first_number) + ' + ' + str(second_number)
        elif operation_type == 3:  # subtraction
            operation = str(first_number) + ' - ' + str(second_number)

        print(operation)
        while True:
            try:
                answer = int(input())
                break
            except ValueError:
                print('Incorrect format.s')

        if operation_type == 1 and first_number * second_number == answer or \
                operation_type == 2 and first_number + second_number == answer or \
                operation_type == 3 and first_number - second_number == answer:
            print('Right!')
            marks += 1
        else:
            print('Wrong!')
elif level == 2:
    for _ in range(5):
        number = random.randint(11, 29)
        print(number)
        while True:
            try:
                answer = int(input())
                break
            except ValueError:
                print('Wrong format! Try again.')

        if answer == number * number:
            print('Right!')
            marks += 1
        else:
            print('Wrong!')

option = input(f'Your mark is {marks}/5. Would you like to save the result? Enter yes or no.')

if option in ('yes', 'YES', 'y', 'Yes'):
    name = input('What is your name?')
    filename = 'results.txt'
    with open(filename, 'a') as file:
        file.write(f'{name}: {marks}/5 in level {level} ({"simple operations with numbers 2-9" if level == 1 else "integral squares of 11-29"}).')
    print(f'The results are saved in "{filename}".')