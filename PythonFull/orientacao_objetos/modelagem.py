# Como escrever conforme a PEP8:
# class PessoasClientes:
#     pass
#
# def pessoas_clientes():
#     pass
#
# Primeiro, para classes e depois para funções.
# E nestes exemplos, usamos nomes duplos.

class Pessoas:
    def __init__(self, nome, idade, cpf):
        self.nome = nome
        self.idade = idade
        self.cpf = cpf

    def logar_sistema(self):
        print(f'{self.nome} está logando no sistema!')


p1 = Pessoas('Caio Sampaio', 21, '123441234')
p2 = Pessoas('Marcos Antônio', 25, '781234934789')
# print(p1)
# print(p2)

print(p1.nome)
print(p1.idade)

print('------')

print(p2.nome)
print(p2.idade)

print('------')

p1.logar_sistema()
p2.logar_sistema()


