arquivo = open('pessoas.txt', 'r')
resultados = [line[:-1] for line in arquivo.readlines()]
print(resultados)
for line in resultados:
    print(line)
    tokens = line.split(' ')
    print(tokens)

print('-------')
x = [i.split() for i in resultados]
print(x)
arquivo.close()
