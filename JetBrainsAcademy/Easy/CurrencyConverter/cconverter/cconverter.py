# write your code here!
import json
import requests

my_currency = input()
data = requests.get(f'http://www.floatrates.com/daily/{my_currency}.json')
dic = json.loads(data.text)
cache = {k: v for k, v in dic.items() if k in ('usd', 'eur')}
your_currency = input()
money = int(input())
while True:
    print('Checking the cache...')
    if your_currency not in cache:
        print('Sorry, but it is not in the cache!')
        cache[your_currency] = dic[your_currency]
    else:
        print('Oh! It is in the cache!')
    value = '{0:.2f}'.format(money * float(cache[your_currency.lower()]['rate']))
    print(f'You received {value} {your_currency}.')
    your_currency = input()
    if your_currency == '':
        break
    money = int(input())
