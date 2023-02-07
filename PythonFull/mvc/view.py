
from controller import PessoaController


while True:
	decisao = int(input('Digite 1 para salvar uma pessoa ou digite 2 para ver a pessoa salva e 3 para sair'))
	if decisao == 3:
		break
	if decisao == 1:
		nome = input('Digite seu nome:')
		idade = int(input('Digite sua idade:'))
		cpf = input('Digite seu CPF:')
		if PessoaController.cadastrar(nome, idade, cpf):
			print('Usuário cadastrado com sucesso.')
		else:
			print('Digite valores válidos!')

# lição de casa
# ver o caso do método de validar CPF na classe PessoaController.
# ver o caso da decisao ser igual a 2, e assim, ver a Pessoa salva.
