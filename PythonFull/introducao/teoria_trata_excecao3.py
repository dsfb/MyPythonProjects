try:
    x = int(input('Digite um número: '))
    print(5 / x)
except Exception as e:
    print(e)
    print("erro interno do sistema!")
