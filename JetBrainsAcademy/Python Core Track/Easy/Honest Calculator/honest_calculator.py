
memory = 0.


def is_one_digit(v):
    try:
        if int(v) != float(v):
            return False

        return -10 < int(v) < 10
    except ValueError:
        return False


def check(v1, v2, v3):
    msg = ''
    if is_one_digit(v1) and is_one_digit(v2):
        msg += " ... lazy"
    
    if (v1 == 1 or v2 == 1) and v3 == '*':
        msg += " ... very lazy"

    if (v1 == 0 or v2 == 0) and v3 in ('+', '-', '*'):
        msg += " ... very, very lazy"

    if msg:
        msg = "You are" + msg
        print(msg)


while True:
    print('Enter an equation')
    equation = input()
    x, oper, y = equation.split(" ")
    try:
        if x == 'M':
            x = memory

        if y == 'M':
            y = memory

        x = float(x)
        y = float(y)
    except ValueError:
        print('Do you even know what numbers are? Stay focused!')
        continue
    
    if oper in ('+', '-', '*', '/'):
        check(x, y, oper)

        if oper == '+':
            result = x + y
        elif oper == '-':
            result = x - y
        elif oper == '*':
            result = x * y
        elif oper == '/':
            if y != 0:
                result = x / y
            else:
                print("Yeah... division by zero. Smart move...")
                continue

        print(result)
        if input('Do you want to store the result? (y / n):') == 'y':
            if is_one_digit(result):
                msg_index = 10
                choice = input("Are you sure? It is only one digit! (y / n)")
                if choice == 'y':
                    choice = input("Don't be silly! It's just one number! Add to the memory? (y / n)")

                if choice == 'y':
                    choice = input("Last chance! Do you really want to embarrass yourself? (y / n)")

                if choice == 'y':
                    memory = result
            else:
                memory = result

        next_case = input('Do you want to continue calculations? (y / n):')
        if next_case == 'y':
            continue
        elif next_case == 'n':
            break
    else:
        print("Yes ... an interesting math operation. You've slept through all classes, haven't you?")
