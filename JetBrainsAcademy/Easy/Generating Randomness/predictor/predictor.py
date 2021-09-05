import random


random.seed()
final_data = ''


while len(final_data) < 100:
    input_data = input('Print a random string containing 0 or 1:')
    for c in input_data:
        if c in ('0', '1'):
            final_data += c
    if len(final_data) < 100:
        print(f'Current data length is {len(final_data)}, {100 - len(final_data)} symbols left')
    else:
        print()

print('Final data string:')
print(final_data)
print()

keys = '000', '001', '010', '011', '100', '101', '110', '111'
counter_dict = {}

for key in keys:
    s_key = final_data.split(key)
    dic = {}
    for num in ('0', '1'):
        counter = 0
        for st in s_key[1:]:
            if st.startswith(num):
                counter += 1
        dic[num] = counter
    counter_dict[key] = (dic['0'], dic['1'])
    # print(key + ': ' + str(dic['0']) + ',' + str(dic['1']))

user_balance = 1000
print()
print(f'You have ${user_balance}. Every time the system successfully predicts your next press, you lose $1.')
print('Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!')
print()

while True:
    print('Print a random string containing 0 or 1:')
    user_str = input()
    if user_str == 'enough':
        break

    if not user_str.isdigit():
        print()
        continue

    print('prediction:')
    predicted_str = ''
    for i in range(3):
        predicted_str += str(random.randint(0, 1))

    i = 0
    while len(predicted_str) < len(user_str):
        key_str = user_str[i:i+3]
        i += 1
        counters = counter_dict[key_str]
        if counters[0] > counters[1]:
            predicted_str += '0'
        elif counters[0] < counters[1]:
            predicted_str += '1'
        else:
            predicted_str += str(random.randint(0, 1))

    counted_predicted_symbols = 0
    for i in range(len(user_str)):
        if i < 3:
            continue
        if user_str[i] == predicted_str[i]:
            counted_predicted_symbols += 1

    counted_symbols = len(user_str) - 3
    percentage_value = round((counted_predicted_symbols / counted_symbols) * 100, 2)
    user_balance += counted_symbols - 2 * counted_predicted_symbols

    print(predicted_str)
    print()
    print(f'Computer guessed right {counted_predicted_symbols} out of {counted_symbols} symbols ({percentage_value} %)')
    print(f'Your balance is now ${user_balance}')
    print()

print('Game over!')
