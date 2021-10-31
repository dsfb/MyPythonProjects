# Faça um programa que o usuário possa cadastrar n pessoas,
# armazenando seu nome, sua idade e sua altura.

pessoas = []
while True:
    decisao = int(input('Digite 1 para cadastrar uma pessoa e 2 para sair: '))
    if decisao == 2:
        break
    # elif decisao == 1:
    #     pass

    nome = input('Digite o nome: ')
    idade = input('Digite a idade: ')
    altura = input('Digite a altura: ')
    pessoa = {'nome': nome,
              'idade': idade,
              'altura': altura}
    pessoas.append(pessoa)

print(pessoas)
