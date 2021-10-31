Python 3.8.10 (default, Sep 28 2021, 16:10:42) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> 
= RESTART: /home/dsfb/More_Documents/python_full_caio_sampaio/introducao/exercicio_cadastrar_pessoas.py
Digite 1 para cadastrar uma pessoa e 2 para sair: 1
Digite o nome: Caio
Digite a idade: 21
Digite a altura: 172
Digite 1 para cadastrar uma pessoa e 2 para sair: 1
Digite o nome: Marcos
Digite a idade: 22
Digite a altura: 175
Digite 1 para cadastrar uma pessoa e 2 para sair: 1
Digite o nome: Pedro
Digite a idade: 34
Digite a altura: 163
Digite 1 para cadastrar uma pessoa e 2 para sair: 2
[{'nome': 'Caio', 'idade': '21', 'altura': '172'}, {'nome': 'Marcos', 'idade': '22', 'altura': '175'}, {'nome': 'Pedro', 'idade': '34', 'altura': '163'}]
>>> pessoa = {'nome': 'danilo', 'idade': 34}
>>> pessoa
{'nome': 'danilo', 'idade': 34}
>>> pessoa.update({'nome': 'Danilo Barbosa', 'idade': 35})
>>> pessoa
{'nome': 'Danilo Barbosa', 'idade': 35}
>>> pessoa
{'nome': 'Danilo Barbosa', 'idade': 35}
>>> pessoa.keys()
dict_keys(['nome', 'idade'])
>>> pessoa.values()
dict_values(['Danilo Barbosa', 35])
>>> pessoa.items()
dict_items([('nome', 'Danilo Barbosa'), ('idade', 35)])
>>> pessoa
{'nome': 'Danilo Barbosa', 'idade': 35}
>>> list(pessoa.items())
[('nome', 'Danilo Barbosa'), ('idade', 35)]
>>> x = _
>>> x
[('nome', 'Danilo Barbosa'), ('idade', 35)]
>>> type(x[0])
<class 'tuple'>
>>> type(pessoa.keys())
<class 'dict_keys'>
>>> type(pessoa.values())
<class 'dict_values'>
>>> type(pessoa.items())
<class 'dict_items'>
>>> type((x for x in range(10)))
<class 'generator'>
>>> for key, value in pessoa.items():
	print(f'key: {key}, e value: {value}')

	
key: nome, e value: Danilo Barbosa
key: idade, e value: 35
>>> or key, value in pessoa.items():
	print(f'key: "{key}", e value: "{value}"')
	
SyntaxError: invalid syntax
>>> for key, value in pessoa.items():
	print(f'key: "{key}", e value: "{value}"')

	
key: "nome", e value: "Danilo Barbosa"
key: "idade", e value: "35"
>>> for key, value in pessoa.items():
	print(f'key: "{key}", e value: "{value}";')

	
key: "nome", e value: "Danilo Barbosa";
key: "idade", e value: "35";
>>> x = [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5]
>>> y = set(x)
>>> x, y
([1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5], {1, 2, 3, 4, 5})
>>> z = 'Daniel'
>>> w = set(z)
>>> w
{'i', 'e', 'a', 'l', 'D', 'n'}
>>> q = list(z)
>>> q
['D', 'a', 'n', 'i', 'e', 'l']
>>> {1. 2, 3, 4, 5} - {5, 7, 8, 9}
SyntaxError: invalid syntax
>>> {1, 2, 3, 4, 5} - {5, 7, 8, 9}
{1, 2, 3, 4}
>>> {1, 2, 3, 4, 5} - {5, 7, 8, 9, 2}
{1, 3, 4}
>>> {1, 2, 3, 4, 5} - {7, 8, 9, 2}
{1, 3, 4, 5}
>>> {1, 2, 3, 4, 5} - {5, 7, 8, 9}
{1, 2, 3, 4}
>>> {1, 2, 3, 4, 5}.symmetric_difference({5, 6, 7, 8, 9})
{1, 2, 3, 4, 6, 7, 8, 9}
>>> {1, 2, 3, 4, 5}.symmetric_difference({5, 6, 7, 8, 9, 2})
{1, 3, 4, 6, 7, 8, 9}
>>> 
