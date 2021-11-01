Python 3.8.10 (default, Sep 28 2021, 16:10:42) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> x = lambda(i: i * 2 + 3)
SyntaxError: invalid syntax
>>> x = lambda i: i * 2 + 3
>>> x(4)
11
>>> import math
>>> y = lambda i: math.sqrt(math.exp(i))
>>> y(4)
7.38905609893065
>>> x = lambda _: print('Ola mundo!')
>>> x()
Traceback (most recent call last):
  File "/usr/lib/python3.8/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#7>", line 1, in <module>
TypeError: <lambda>() missing 1 required positional argument: '_'
>>> x = lambda: print('Olá mundo!')
>>> x()
Olá mundo!
>>> type(x)
<class 'function'>
>>> x = lambda nome, idade: print(f"nome = {nome}\n idade = {idade}.")
>>> x('Danilo', 24)
nome = Danilo
 idade = 24.
>>> x = lambda nome, idade: print(f"nome = {nome}\nidade = {idade}.")
>>> x('Caio', 20)
nome = Caio
idade = 20.
>>> x = lambda nome, idade: print(f"nome = {nome}\nidade = {idade}")
>>> x('Caio', 20)
nome = Caio
idade = 20
>>> x = lambda *args: print(args)
>>> x('caio', 'marcos', 'joao')
('caio', 'marcos', 'joao')
>>> x('caio')
('caio',)
>>> x()
()
>>> def f():
	return 'caio', 'marcos'

>>> x(f)
(<function f at 0x7f941b161e50>,)
>>> x(f())
(('caio', 'marcos'),)
>>> x(*f)
Traceback (most recent call last):
  File "/usr/lib/python3.8/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#26>", line 1, in <module>
TypeError: <lambda>() argument after * must be an iterable, not function
>>> def teste():
	return lambda *args: print(args)

>>> x = teste()
>>> print(x)
<function teste.<locals>.<lambda> at 0x7f941a0d8160>
>>> x('caio', 'marcos')
('caio', 'marcos')
>>> 