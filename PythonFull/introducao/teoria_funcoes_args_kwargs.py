Python 3.8.10 (default, Sep 28 2021, 16:10:42) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> def soma(n1, n2):
	print(n1 + n2)

	
>>> soma(5, 2)
7
>>> soma(n2=5, n1=2)
7
>>> def somaa(*args):
	print(sum(args))

	
>>> somaa(5, 2, 3, 4, 5, 6, 8, 9)
42
>>> def somak(**kwargs):
	print(sum(kwargs['numeros']))

	
>>> somak(numeros=[1, 2, 4, 5, 9, 12])
33
>>> 