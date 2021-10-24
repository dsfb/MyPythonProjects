# Write your code here


class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.coffee = 120
        self.cups = 9
        self.money = 550

    def remaining(self):
        print()
        print('The coffee machine has:')
        print('{} of water'.format(self.water))
        print('{} of milk'.format(self.milk))
        print('{} of coffee beans'.format(self.coffee))
        print('{} of disposable cups'.format(self.cups))
        print('${} of money'.format(self.money))

    def take(self):
        print('I gave you ${}'.format(self.money))
        self.money = 0

    def fill(self):
        self.water += int(input('Write how many ml of water do you want to add:'))
        self.milk += int(input('Write how many ml of milk do you want to add:'))
        self.coffee += int(input('Write how many grams of coffee beans do you want to add:'))
        self.cups += int(input('Write how many disposable cups of coffee do you want to add:'))

    def buy(self):
        option = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')

        if option == 'back':
            return
        else:
            option = int(option)

        result, not_enough = self.is_available(option)
        if not result:
            print(not_enough)
            print()
        elif option == 1:
            self.water -= 250
            self.coffee -= 16
            self.cups -= 1
            self.money += 4
        elif option == 2:
            self.water -= 350
            self.milk -= 75
            self.coffee -= 20
            self.cups -= 1
            self.money += 7
        elif option == 3:
            self.water -= 200
            self.milk -= 100
            self.coffee -= 12
            self.cups -= 1
            self.money += 6

        print('I have enough resources, making you a coffee!')
        print()

    def is_available(self, option):
        not_enough = ''
        if option == 1:
            if self.water - 250 < 0:
                not_enough = 'Sorry, not enough water!'
                return False, not_enough
            if self.coffee - 16 < 0:
                not_enough = 'Sorry, not enough coffee!'
                return False, not_enough
            if self.cups < 1:
                not_enough = 'Sorry, not enough cup!'
                return False, not_enough
        elif option == 2:
            if self.water - 350 < 0:
                not_enough = 'Sorry, not enough water!'
                return False, not_enough
            if self.milk - 75 < 0:
                not_enough = 'Sorry, not enough milk!'
                return False, not_enough
            if self.coffee - 20 < 0:
                not_enough = 'Sorry, not enough coffee!'
                return False, not_enough
            if self.cups < 1:
                not_enough = 'Sorry, not enough cup!'
                return False, not_enough
        elif option == 3:
            if self.water - 200 < 0:
                not_enough = 'Sorry, not enough water!'
                return False, not_enough
            if self.milk - 100 < 0:
                not_enough = 'Sorry, not enough milk!'
                return False, not_enough
            if self.coffee - 12 < 0:
                not_enough = 'Sorry, not enough coffee!'
                return False, not_enough
            if self.cups < 1:
                not_enough = 'Sorry, not enough cup!'
                return False, not_enough
        return True, not_enough


def get_action():
    return input('Write action (buy, fill, take, remaining, exit): ')


if __name__ == "__main__":
    c = CoffeeMachine()

    action = get_action()

    while action != 'exit':
        if action == 'buy':
            c.buy()
        elif action == 'fill':
            c.fill()
        elif action == 'take':
            c.take()
        elif action == 'remaining':
            c.remaining()
        elif action == 'exit':
            pass

        action = get_action()
