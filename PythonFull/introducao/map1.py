import math

x = [i for i in range(12, 26)]

x = list(map(lambda x: 10 if x < 18 else x, x))

print(x)

x = list(map(lambda x: math.sqrt(x) if x % 2 == 0 else math.exp(x), x))

print(x)

x = [{'nome': 'caio', 'idade': 20}, {'nome': 'marcos', 'idade': 40}]

x = list(map(lambda x: {'nome': x['nome'], 'idade': 'menor do que 38 anos'} if x['idade'] < 38 else x, x))

print(x)

print('------')

x = [{'nome': 'caio', 'idade': 20}, {'nome': 'marcos', 'idade': 22}]

x = list(map(lambda x: {'nome': x['nome'], 'idade': 'menor do que 38 anos'} if x['idade'] < 38 else x, x))

print(x)

print('------')

x = [{'nome': 'caio', 'idade': 20}, {'nome': 'marcos', 'idade': 40}]

x = list(map(lambda x: {'nome': x['nome'], 'idade': 'menor do que 38 anos' if x['idade'] < 38 else x['idade']}, x))

print(x)
