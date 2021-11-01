from pympler.asizeof import asizesof

print('size of an int:')
print(asizesof(1))
print(asizesof(1234))
print(asizesof(1999999999999999999999990000000000000000000000))
print(asizesof(999889888889899998989899898989899999999999999999999999999))

print('size of a float:')
print(asizesof(1.))
print(asizesof(3.141592))
print(asizesof(3.1415926535897932384626433))
print(asizesof(2.718281828459045235360287))
print(asizesof(177456678976.12))

print('size of a string:')
print(asizesof('asdf'))
print(asizesof(''))
print(asizesof('asfddasdfasdfaasdfasdfasdfasdfasdfasdfhjasdfhadfasdfhjasdfsdfasdfasdfsdasdfasdfdhasdfasdfasdfasdf'))

print('size of a list:')
print(asizesof([]))
print(asizesof([1]))
print(asizesof([1, 2]))
print(asizesof([1, 2, 3]))

print('size of a tuple:')
print(asizesof(()))

def dobro(lista):
    lista_dobro = []
    for i in lista:
        lista_dobro.append(i * 2)
    return lista_dobro

x = asizesof(dobro(range(0, 100)))

print(x)
print(type(dobro(range(0, 100))))


def dobrou():
    yield 1


print(type(dobrou()))
print(next(dobrou()))
print(next(dobrou()))
print(next(dobrou()))


def dobrou():
    yield 1
    yield 2
    yield 3


print(next(dobrou()))
print(next(dobrou()))
print(next(dobrou()))
print(next(dobrou()))

try:
    d = dobrou()
    print(next(d))
    print(next(d))
    print(next(d))
    print(next(d))
except StopIteration:
    print('StopIteration...!')
    pass

print('Deu exception? Sim! ;)')


def dobrou():
    i = 0
    while True:
        i = i + 1
        yield i


x = dobrou()
while True:
    y = next(x)
    if y > 100:
        break

    print(next(x))


def dobrou2(lista):
    for i in lista:
        yield i * 2


def dobrou3(lista):
    return [i * 2 for i in lista]


x = dobrou2(range(0, 10000))

y = dobrou3(range(0, 10000))

print('size x: ' + str(asizesof(x)[0]))
print('size y: ' + str(asizesof(y)[0]))

y = dobrou3(range(0, 100000))
x = dobrou2(range(0, 100000))

print('size x: ' + str(asizesof(x)[0]))
print('size y: ' + str(asizesof(y)[0]))


def dobrou(lista):
    for i in lista:
        yield i * 2


x = dobrou(range(0, 100))

while True:
    try:
        print(next(x))
    except StopIteration:
        break

x = dobrou(range(0, 100))

print('---------')

for i in x:
    print(i)
