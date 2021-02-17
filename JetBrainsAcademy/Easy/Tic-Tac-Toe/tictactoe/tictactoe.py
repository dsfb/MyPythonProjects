# write your code here

   
def analyse_game(cells):
    o_count = cells.count('O')
    x_count = cells.count('X')
    if x_count - o_count > 1 or o_count - x_count > 1:
        return 'Impossible'
    x_wins = 'X wins'
    o_wins = 'O wins'

    for i in range(3):
        if cells[3 * i] == cells[3 * i + 1] == cells[3 * i + 2]:
            if cells[3 * i] == 'O':
                return o_wins
            elif cells[3 * i] == 'X':
                return x_wins
            elif cells[3 * i] != ' ':
                return 'Impossible'
        elif cells[i] == cells[i + 3] == cells[i + 6]:
            if cells[i] == 'O':
                return o_wins
            elif cells[i] == 'X':
                return x_wins
            elif cells[i] != ' ':
                return 'Impossible'

    if cells[0] == cells[4] == cells[8]:
        if cells[4] == 'X':
            return x_wins
        elif cells[4] == 'O':
            return o_wins
    elif cells[2] == cells[4] == cells[6]:
        if cells[4] == 'X':
            return x_wins
        elif cells[4] == 'O':
            return o_wins

    if cells.count(' ') > 0:
        return 'Game not finished'

    return 'Draw'


def enter_playing():
    return input('Enter the coordinates: ')


def process_playing(coordinates):
    return list(map(int, coordinates.split(" ")))


def show_table(cells):
    print("---------")
    for x in range(3):
        print("| {} {} {} |".format(cells[x * 3], cells[x * 3 + 1], cells[x * 3 + 2]))
    print("---------")


def check_occupied_cell(cells, coordinates):
    return cells[(coordinates[0] - 1) * 3 + coordinates[1] - 1] != ' '


def check_range(coordinates):
    for coordinate in coordinates:
        if coordinate < 1 or coordinate > 3:
            return False
    return True


def process_the_turn(cells, coordinates, char_turn):
    try:
        if not check_range(coordinates):
            return 1

        if not check_occupied_cell(cells, coordinates):
            cells[(coordinates[0] - 1) * 3 + coordinates[1] - 1] = char_turn
        else:
            return 2
        return 0
    except IndexError:
        return 1


def change_char_turn(char_turn):
    if char_turn == 'X':
        return 'O'
    elif char_turn == 'O':
        return 'X'

    return ''

def process_game():
    cells = [' ', ] * 9
    show_table(cells)
    char_turn = 'X'
    while True:
        try:
            coordinates = enter_playing()
            coordinates = process_playing(coordinates)
            result = process_the_turn(cells, coordinates, char_turn)
            if result == 0:
                show_table(cells)
                result_str = analyse_game(cells)
                if result_str != 'Game not finished':
                    print(result_str)
                    break

                char_turn = change_char_turn(char_turn)
            elif result == 1:
                print('Coordinates should be from 1 to 3!')
            elif result == 2:
                print('This cell is occupied! Choose another one!')
        except ValueError:
            print('You should enter numbers!')


if __name__ == '__main__':
    process_game()    
