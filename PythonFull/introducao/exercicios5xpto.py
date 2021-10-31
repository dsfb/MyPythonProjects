Python 3.8.10 (default, Sep 28 2021, 16:10:42) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> n = 4
>>> iterador = 1
>>> iterador = 0
>>> while iterador <= 10:
	print(f'{n} x {iterador} = {n * iterador}')
	iterador += 1


4 x 0 = 0
4 x 1 = 4
4 x 2 = 8
4 x 3 = 12
4 x 4 = 16
4 x 5 = 20
4 x 6 = 24
4 x 7 = 28
4 x 8 = 32
4 x 9 = 36
4 x 10 = 40
>>> n = -1
>>> if n < 0 or n > 10:
	print('Digite de novo!')


Digite de novo!
>>> n = 4
>>> if n < 0 or n > 10:
	print('Digite de novo!')
else:
	print('Ok!')


Ok!
>>> n = -1
>>> if n < 0 or n > 10:
	print('Digite de novo!')
else:
	print('Ok!')


Digite de novo!
>>> n = 12
>>> if n < 0 or n > 10:
	print('Digite de novo!')
else:
	print('Ok!')


Digite de novo!
>>> n = 7
>>> if n < 0 or n > 10:
	print('Digite de novo!')
else:
	print('Ok!')


Ok!
>>> usuario = 'danilo'
>>> senha = 'estrelaDalva'
>>> while True:
	user = input('Digite usuario: ')
	password = input('Digite senha: ')
	if user == usuario and senha == password:
		print('Login feito com sucesso!')
	print('Login inválido! Tente novamente!')

	
Digite usuario: sara
Digite senha: aba
Login inválido! Tente novamente!
Digite usuario: danilo
Digite senha: aba
Login inválido! Tente novamente!
Digite usuario: sara
Digite senha: estrelaDalva
Login inválido! Tente novamente!
Digite usuario: danilo
Digite senha: estrelaDalva
Login feito com sucesso!
Login inválido! Tente novamente!
Digite usuario: 
Traceback (most recent call last):
  File "/usr/lib/python3.8/idlelib/run.py", line 559, in runcode
    exec(code, self.locals)
  File "<pyshell#33>", line 2, in <module>
  File "/usr/lib/python3.8/idlelib/run.py", line 484, in readline
    line = self._line_buffer or self.shell.readline()
  File "/usr/lib/python3.8/idlelib/rpc.py", line 607, in __call__
    value = self.sockio.remotecall(self.oid, self.name, args, kwargs)
  File "/usr/lib/python3.8/idlelib/rpc.py", line 219, in remotecall
    return self.asyncreturn(seq)
  File "/usr/lib/python3.8/idlelib/rpc.py", line 248, in asyncreturn
    response = self.getresponse(seq, wait=0.05)
  File "/usr/lib/python3.8/idlelib/rpc.py", line 291, in getresponse
    response = self._getresponse(myseq, wait)
  File "/usr/lib/python3.8/idlelib/rpc.py", line 319, in _getresponse
    cvar.wait()
  File "/usr/lib/python3.8/threading.py", line 302, in wait
    waiter.acquire()
KeyboardInterrupt
>>> while True:
	user = input('Digite usuario: ')
	password = input('Digite senha: ')
	if user == usuario and senha == password:
		print('Login feito com sucesso!')
		break
	print('Login inválido! Tente novamente!')

	
Digite usuario: sara
Digite senha: abv
Login inválido! Tente novamente!
Digite usuario: danilo
Digite senha: estrelaDalva
Login feito com sucesso!
>>> 
