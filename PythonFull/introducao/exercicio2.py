nota1 = float(input('Digite a primeira nota: '))
nota2 = float(input('Digite a segunda nota: '))
nota3 = float(input('Digite a terceira nota: '))
nota4 = float(input('Digite a quarta nota: '))

media = (nota1 + nota2 + nota3 + nota4) / 4
print(f'A média é: {media}')

if media >= 6:
    print('Aprovado!')
elif media >= 4:
    print('Em recuperação!')
else:
    print('Reprovado!')
