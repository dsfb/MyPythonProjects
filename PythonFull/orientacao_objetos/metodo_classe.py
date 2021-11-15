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

    @classmethod
    def andar(cls, velocidade):
        print(f'Estou andando com velocidade {velocidade} m/s.')

p1 = Pessoas('Caio Sampaio', 21)
p2 = Pessoas("Marcos Sampaio", 22)

p1.logar_sistema()

Pessoas.andar(23)
p1.andar(35)


