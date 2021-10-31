from minha_lib import x as x_importado
from minha_lib import minha_soma
from minhas_funcoes.minha_lib import soma_numeros as soma
from minhas_funcoes.minha_lib import subtrai_numeros as subtrai

x = 50

print(x, x_importado)
print(minha_soma(4, 2))
print(soma(5, 3))
print(subtrai(15, 2))

