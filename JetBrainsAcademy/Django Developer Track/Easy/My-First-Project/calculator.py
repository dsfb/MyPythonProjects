
# Product dict with key: name, and value: price.
product_info = {
    'Bubblegum': 202,
    'Toffee': 118,
    'Ice cream': 2250,
    'Milk chocolate': 1680,
    'Doughnut': 1075,
    'Pancake': 80
}


def display_message(msg="Prices:"):
    print(msg)


def display_list_all_products():
    for name, price in product_info.items():
        print(f'{name}: ${price}')


def get_income():
    return float(sum(product_info.values()))


def display_income():
    income = get_income()
    print(f'Income: ${ income }')


def get_expenses(expenses_msg):
    expenses = float(input(expenses_msg))
    return expenses


def get_staff_expenses():
    expenses_msg = 'Staff expenses:'
    return get_expenses(expenses_msg)


def get_other_expenses():
    expenses_msg = 'Other expenses:'
    return get_expenses(expenses_msg)


def calculate_net_income(income,
                         staff_expenses,
                         other_expenses):
    result = income - staff_expenses
    result -= other_expenses
    return result


def display_net_income(net_income):
    print(f'Net income: ${ net_income }')


def display_earned_amount():
    display_message('Earned amount:')
    display_list_all_products()
    print()
    display_income()


def process_net_income():
    income = get_income()
    staff_expenses = get_staff_expenses()
    other_expenses = get_other_expenses()
    net_income = calculate_net_income(income,
                                      staff_expenses,
                                      other_expenses)
    display_net_income(net_income)


if __name__ == '__main__':
    display_earned_amount()
    process_net_income()
