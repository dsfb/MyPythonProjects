class Pessoas:
    def __init__(self, nome):
        nome_pessoas = nome

    def logar_sistema(self):
        print(f'Estou logando no sistema.')

if False:
    # Caso de erro abordado na aula anteriormente!
    p1 = Pessoas('Caio Sampaio')
    print(p1.nome_pessoas)


class Pessoas:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def retorna_nome(self):
        return self.nome

    def logar_sistema(self):
        print(f'{self.retorna_nome()} está logando no sistema.')


p1 = Pessoas('Caio Sampaio', 21)
p2 = Pessoas('Marcos Sampaio', 21)

# print(p1.nome)
p1.logar_sistema()
p2.logar_sistema()

