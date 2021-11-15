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
    def andar(cls):
        # Obs.: este método já retorna None! ;)
        cls.pernas = 2

    @classmethod
    def queimar_boca(cls):  # Risos!
        # Obs.: já retorna None!
        cls.possui_boca = False

    @staticmethod
    def é_adulto(idade):
        return idade > 18


print(Pessoas.é_adulto(21))
