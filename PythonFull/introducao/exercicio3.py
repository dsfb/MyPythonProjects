num1 = float(input("Digite o primeiro número: "))
num2 = float(input('Digite o segundo número: '))
num3 = float(input('Digite o terceiro número: '))

print(f'O maior número entre estes três é: {max(num1, num2, num3)};')

if num1 > num2 and num1 > num3:
    print(f'Num1 é o maior: {num1}')
elif num2 > num1 and num2 > num3:
    print(f'Num2 é o maior: {num2}')
else:
    print(f'Num3 é o maior: {num3}')

