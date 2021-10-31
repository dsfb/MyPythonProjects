Python 3.8.10 (default, Sep 28 2021, 16:10:42) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> x = 2 + 1 - 3
>>> x
0
>>> if x:
	print('Aceitou o zero! Viu?')
else:
	print('Opa! Tratou o zero como False! ;)')

	
Opa! Tratou o zero como False! ;)
>>> dic = {'0': 0}
>>> dic.get(1) is None
True
>>> {0: 0}.get(1) is None
True
>>> {0: 0}.get(0) is not None
True
>>> 