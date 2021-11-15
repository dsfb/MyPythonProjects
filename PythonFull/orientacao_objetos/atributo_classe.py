class Pessoas:
    possui_olho = True
    possui_boca = True
    raca = "Ser humano"

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def retorna_nome(self):
        return self.nome

    def logar_sistema(self):
        print(f'{self.retorna_nome()} está logando no sistema.')


# Instruções que darão erros!
# print(Pessoas.nome)
# print(Pessoas.self.nome)
# print(Pessoas.retorna_nome())
# print(Pessoas.retorna_nome('Caio'))

print(Pessoas.possui_olho)
print(Pessoas.possui_boca)
print(Pessoas.raca)

p1 = Pessoas('Caio Sampaio', 21)
p1.possui_olho = False
print(p1.retorna_nome())
print(p1.possui_olho)

p2 = Pessoas("Marcos Sampaio", 22)
print(p2.retorna_nome())
print(p2.possui_olho)

print('Mudando o atributo da classe...')
Pessoas.possui_olho = False
print(p1.retorna_nome())
print(p1.possui_olho)

print(p2.retorna_nome())
print(p2.possui_olho)
