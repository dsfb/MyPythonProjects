
def check_num_of_pencils(num_of_pencils):
    if num_of_pencils.isalpha():
        print('The number of pencils should be numeric')
        return False
    elif num_of_pencils.isdigit():
        value = int(num_of_pencils)
        if value == 0:
            print('The number of pencils should be positive')
            return False
        elif value > 0:
            return True
    else:
        print('The number of pencils should be numeric')
        return False


def process_num_of_pencils():
    num_of_pencils = input('How many pencils would you like to use:')
    while not check_num_of_pencils(num_of_pencils):
        num_of_pencils = input()
    return int(num_of_pencils)


def check_first_player_name(first_player_name):
    if not first_player_name.isalpha():
        print("Choose between 'John' and 'Jack'")
        return False
    elif first_player_name not in ('John', 'Jack'):
        print("Choose between 'John' and 'Jack'")
        return False

    return True


def process_first_player_name():
    first_player_name = input('Who will be the first (John, Jack):')
    while not check_first_player_name(first_player_name):
        first_player_name = input()
    return first_player_name


def check_first_player_playing(player_playing):
    if player_playing not in ('1', '2', '3'):
        print("Possible values: '1', '2' or '3'")
        return False
    elif int(player_playing) > num_of_pencils:
        print('Too many pencils were taken')
        return False

    return True


def process_first_player_choice():
    player_choice = input()
    while not check_first_player_playing(player_choice):
        player_choice = input()
    return player_choice


def process_second_player_choice():
    if (num_of_pencils - 1) % 4 == 0:
        # losing position
        player_choice = '1'
    else:
        # winning position
        player_choice = str((num_of_pencils - 1) % 4)

    return player_choice


num_of_pencils = process_num_of_pencils()

first_player_name = process_first_player_name()

john_turn = first_player_name == 'John'
player_choice = 0

while num_of_pencils > 0:
    print('|' * num_of_pencils)
    print(f'{"John" if john_turn else "Jack"}\'s turn!')
    if john_turn:
        player_choice = process_first_player_choice()
        num_of_pencils -= int(player_choice)
    else:
        player_choice = process_second_player_choice()
        num_of_pencils -= int(player_choice)
        print(player_choice)

    if num_of_pencils == 0:
        print(f'{"John" if not john_turn else "Jack"} won!')
        break

    john_turn = not john_turn
