import pickle

# x = [1, 2, 3, 4]

# input("Digite algo: ")

x = 1
print(x)
print(type(x))
print(pickle.dumps(x))

x = [1, 2, 3, 4]
string = pickle.dumps(x)
print(type(string))

print(pickle.loads(string))
print(type(pickle.loads(string)))

x = {'nome': 'caio', 'idade': 20}

string = pickle.dumps(x)
print(pickle.loads(string)['nome'])

x = [1, 2, 3, 4, 'Mônica']

arq = open('arquivo.pkl', 'wb')
pickle.dump(x, arq)
arq.close()
print('O arquivo foi escrito.')

arq = open('arquivo.pkl', 'rb')
y = pickle.load(arq)
arq.close()
print('O arquivo foi lido.')
print(y)
print('y == x ? R.:')
print(y == x)
print('y is x ? R.:')
print(y is x)


class Pessoa:
    nome = 'Caio'
    idade = 20

arq = open('arquivo.pkl', 'wb')
# pickle.dump(Pessoa, arq)
arq.close()

arq = open('arquivo.pkl', 'rb')
# retornou = pickle.load(arq)
arq.close()

# print(retornou)
# print(retornou.nome)
# print(retornou.idade)


class Pessoas:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

p1 = Pessoas('marcos', 21)

arq = open('arquivo.pkl', 'ab')
# pickle.dump(p1, arq)
pickle.dump([1, 2, 3, 4], arq)
arq.close()

arq = open('arquivo.pkl', 'rb')
retornou = pickle.load(arq)
# retornou2 = pickle.load(arq)
# retornou3 = pickle.load(arq)
arq.close()

# print(retornou.nome)
# print(retornou2.nome)
# print(retornou3.nome)
print(retornou)


with open('arquivo.pkl', 'wb') as arq:
    pickle.dump(p1, arq)


with open('arquivo.pkl', 'rb') as arq:
    p2 = pickle.load(arq)
    print('nome:')
    print(p2.nome)
