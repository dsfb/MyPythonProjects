# Write your code here

import math
import os
import sys
import random
import sqlite3

from datetime import datetime
random.seed(datetime.now())

number = 4000004938320811

accounts = {}

logged = False
logged_number = 0

balances = {}

def process_luhn(num):
    string = str(num)[:-1]
    the_list = list(string)
    the_list = [int(elem) * 2 if index % 2 == 0 else int(elem) for index, elem in enumerate(the_list)]
    the_list = [elem if elem < 10 else elem - 9 for _, elem in enumerate(the_list)]
    value = 10 - sum(the_list) % 10
    num = num // 10
    num = num * 10 + value
    return num


def create():
    global number
    my_number = process_luhn(number)
    accounts[my_number] = str(random.randrange(0, 10000))
    val = accounts[my_number]
    while len(val) < 4:
        val = '0' + val
        accounts[my_number] = val
    print('Your card has been created')
    print('Your card number:')
    print(my_number)
    print('Your card PIN:')
    print(accounts[my_number])
    cur.execute(f'INSERT INTO card (number, pin, balance) VALUES ({my_number}, {accounts[my_number]}, "0")')
    conn.commit()
    number = my_number + int(math.pow((11, 13, 17, 19)[random.randint(0, 3)], 3))


def login():
    global logged
    global logged_number
    print('Enter your card number:')
    num = int(input())
    print('Enter your PIN:')
    key = input()
    if num in accounts and accounts[num] == key:
        print('You have successfully logged in!')
        logged_number = num
        logged = True
    else:
        print('Wrong card number or PIN!')


def logout():
    global logged
    print('You have successfully logged out!')
    logged = False


def get_balance(the_number):
    query = f'SELECT balance FROM card WHERE number = "{the_number}"'
    print(f'get balance query: {query}')
    result = cur.execute(query)
    row = cur.fetchone()
    return int(row[0])


def process_income(income, the_number):
    balance = get_balance(the_number) + income
    result = cur.execute(f'UPDATE card SET balance = {balance} WHERE number = "{the_number}"')
    conn.commit()
    print('Income was added!')

def add_income():
    income = int(input('Enter income:'))
    process_income(income, logged_number)


def do_transfer():
    print('Transfer')
    the_number = int(input('Enter card number:'))
    if the_number != process_luhn(the_number):
        print('Probably you made mistake in card number. Please try again!')
        return None
    result = cur.execute(f'SELECT COUNT(*) FROM card WHERE number = {the_number}')
    if int(cur.fetchone()[0]) == 0:
        print('Such a card does not exist.')
        return None
    money = int(input('Enter how much money you want to transfer:'))
    balance = get_balance(logged_number)
    if balance < money:
        print('Not enough money!')
    else:
        process_income(-money, logged_number)
        process_income(money, the_number)
        print('Success!')


def close_account():
    result = cur.execute(f'DELETE FROM card WHERE number = "{logged_number}"')
    conn.commit()
    logout()
    print('The account has been closed!')


def logged_menu():
    print('1. Balance')
    print('2. Add income')
    print('3. Do transfer')
    print('4. Close account')
    print('5. Log out')
    print('0. Exit')


def menu():
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')


def show_balance():
    result = cur.execute(f'SELECT balance FROM card WHERE number = {logged_number}')
    row = cur.fetchone()
    print(f'Balance: {row["balance"]}')


def logged_option():
    logged_menu()
    x = int(input())
    if x == 0:
        exit()
    elif x == 1:
        show_balance()
    elif x == 2:
        add_income()
    elif x == 3:
        do_transfer()
    elif x == 4:
        close_account()
    elif x == 5:
        logout()


def option():
    menu()
    x = int(input())
    if x == 0:
        exit()
    elif x == 1:
        create()
    elif x == 2:
        login()


def exit():
    cur.close()
    conn.close()
    sys.exit(0)


database_filename = 'card.s3db'
creation_query = '''CREATE TABLE IF NOT EXISTS card(
        id INTEGER PRIMARY KEY,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
    );'''

database_full_file = database_filename

f = open(database_full_file, "w")
f.close()
conn = sqlite3.connect(database_full_file)
cur = conn.cursor()
result = cur.execute(creation_query)
conn.commit()

result = cur.execute('SELECT number, pin, balance FROM card')
rows = cur.fetchall()

for row in rows:
    accounts[row['number']] = row['pin']
    balances[row['number']] = row['balance']

while True:
    if logged:
        logged_option()
    else:
        option()
