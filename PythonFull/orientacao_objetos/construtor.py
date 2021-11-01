class Pessoas:
    def __init__(self, nome, idade, cpf):
        print(f'{nome} | {idade} | {cpf}')

    def logar_sistema(self):
        print('Estou logando no sistema!')


p1 = Pessoas('Caio Sampaio', 21, '12341')
# p1.logar_sistema()

p2 = Pessoas('Marcos Sampaio', 45, '1423123')
