# write your code here
import random

try:
    number = int(input("Enter the number of friends joining (including you):"))
    print()
    if number <= 0:
        print("No one is joining for the party")
    else:
        print("Enter the name of every friend (including you), each on a new line:")
        dic_people = dict()
        for _ in range(number):
            dic_people[input()] = 0
        print()
        bill = int(input("Enter the total bill value:"))
        value = round(float(bill) / number, 2)
        for people in dic_people:
            dic_people[people] = value
        print()
        lucky_feature = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
        print()
        if lucky_feature == 'No':
            print('No one is going to be lucky')
        elif lucky_feature == 'Yes':
            lucky_person = random.choice(list(dic_people.keys()))
            print(f'{lucky_person} is the lucky one!')
            value = float(dic_people[lucky_person])
            divided_value = value / (number - 1)
            dic_people[lucky_person] = 0.
            for person in dic_people:
                if person != lucky_person:
                    dic_people[person] = dic_people[person] + divided_value

        print()
        print(dic_people)
except ValueError:
    print("No one is joining for the party")