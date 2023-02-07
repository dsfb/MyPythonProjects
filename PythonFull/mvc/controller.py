
from dao import PessoaDal
from model import Pessoa

class PessoaController:
	@classmethod
	def cpf_valido(cls, cpf):
		# lição de casa
		pass

	@classmethod
	def cadastrar(cls, nome, idade: int, cpf):
		if len(nome) > 2 and (idade > 0 and idade < 200) and \
			len(cpf) == 11:
			try:
				PessoaDal.salvar(Pessoa(nome, idade, cpf))
				return True
			except:
				return False
		else:
			return False


PessoaController.cadastrar('caio', 20, '12345444444')
