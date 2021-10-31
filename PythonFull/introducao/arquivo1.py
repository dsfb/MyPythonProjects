arquivo = open('pessoas.txt', 'a')
i = 0
while True:
    if i > 4:
        break
    arquivo.write(input('Digite o nome da pessoa: ') + '\n')
    i += 1
arquivo.close()
