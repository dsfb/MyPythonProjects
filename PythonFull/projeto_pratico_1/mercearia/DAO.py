from Models import *


class Dao:
    dado = list()

    @classmethod
    def salvar(cls, dado, filename):
        if isinstance(dado, list):
            dado = '|'.join(list(map(lambda x: x if isinstance(x, str) else str(x), dado)))

        with open(filename, 'a') as arq:
            arq.writelines(dado)
            arq.writelines('\n')

    @classmethod
    def ler(cls, filename):
        with open(filename, 'r') as arq:
            cls.dado = arq.readlines()

            cls.dado = list(map(lambda x: x.replace('\n', ''), cls.dado))
            if cls.dado and '|' in cls.dado[0]:
                cls.dado = list(map(lambda x: x.split('|'), cls.dado))

            return cls.dado


class DaoCategoria(Dao):
    filename = 'categoria.txt'

    @classmethod
    def salvar(cls, categoria):
        super(DaoCategoria, cls).salvar(categoria, cls.filename)

    @classmethod
    def ler(cls):
        cls.categoria = super(DaoCategoria, cls).ler(cls.filename)

        return [Categoria(cat) for cat in cls.categoria]


# DaoCategoria.salvar("Verduras")
# DaoCategoria.salvar("Legumes")
# DaoCategoria.salvar("Carros")
# print(DaoCategoria.ler())

class DaoVenda(Dao):
    filename = 'venda.txt'

    @classmethod
    def salvar(cls, venda: Venda):
        dado_venda = [venda.itensVendido.nome, venda.itensVendido.preco,
         venda.itensVendido.categoria, venda.vendedor,
         venda.comprador, venda.quantidadeVendida,
         venda.data]

        super(DaoVenda, cls).salvar(dado_venda, cls.filename)

    @classmethod
    def ler(cls):
        cls.vendas = super(DaoVenda, cls).ler(cls.filename)

        return [Venda(Produtos(*ven[0:3]), *ven[3:]) for ven in cls.vendas]


# p = Produtos('Banana Prata', '5', 'frutas')
# v = Venda(p, 'Caio', 'Marcos', 3)
# DaoVenda.salvar(v)
# print(DaoVenda.ler())

# p = Produtos('Laranja', '4', 'frutas')
# v = Venda(p, 'Caio', 'Lucas', 3)
# DaoVenda.salvar(v)
# print(DaoVenda.ler())

# p = Produtos('Abacaxi', '3', 'frutas')
# v = Venda(p, 'Caio', 'Paulo', 5)
# DaoVenda.salvar(v)
# print(DaoVenda.ler())

# x = DaoVenda.ler()
# print(x)
# print(x[-1])
# print(x[-1].comprador)
# print(x[-1].itensVendido.nome)

# No padrão MVC, é normal termos códigos parecidos entre as DAOs.
# E não adianta colocarmos uma classe abstrata, ou uma função auxiliar,
# pois isto foge do padrão MVC clássico.
# Assim, vamos fazer o restante das DAOs, com código parecido, e repetido
#  "de certa forma".


class DaoEstoque(Dao):
    filename = 'estoque.txt'

    @classmethod
    def salvar(cls, produto: Produtos, quantidade):
        dado_produto = [produto.nome, produto.preco,
                                produto.categoria, quantidade]

        super(DaoEstoque, cls).salvar(dado_produto, cls.filename)

    @classmethod
    def ler(cls):
        with open(cls.filename, 'r') as arq:
            cls.estoques = super(DaoEstoque, cls).ler(cls.filename)

            return [Estoque(Produtos(*est[0:3]), *est[3:]) for est in cls.estoques]


class DaoFornecedor(Dao):
    filename = 'fornecedores.txt'

    @classmethod
    def salvar(cls, fornecedor: Fornecedor):
        dado_fornecedor = [fornecedor.nome, fornecedor.cnpj, fornecedor.telefone,
                           fornecedor.categoria]

        super(DaoFornecedor, cls).salvar(dado_fornecedor, cls.filename)

    @classmethod
    def ler(cls):
        cls.fornecedores = super(DaoFornecedor, cls).ler(cls.filename)

        return [Fornecedor(*fornec) for fornec in cls.fornecedores]


class DaoPessoa(Dao):
    filename = 'clientes.txt'

    @classmethod
    def salvar(cls, pessoa: Pessoa):
        dado_pessoa = [pessoa.nome, pessoa.telefone, pessoa.cpf]

        super(DaoPessoa, cls).salvar(dado_pessoa, cls.filename)

    @classmethod
    def ler(cls):
        cls.clientes = super(DaoPessoa, cls).ler(cls.filename)

        return [Pessoa(*pes) for pes in cls.clientes]


class DaoFuncionario(Dao):
    filename = 'funcionarios.txt'

    @classmethod
    def salvar(cls, funcionario: Funcionario):
        dado_funcionario = [funcionario.clt, funcionario.nome, funcionario.telefone,
                             funcionario.cpf, funcionario.email, funcionario.endereco]

        super(DaoFuncionario, cls).salvar(dado_funcionario, cls.filename)

    @classmethod
    def ler(cls):
        cls.funcionarios = super(DaoFuncionario, cls).ler(cls.filename)

        return [Funcionario(*func) for func in cls.funcionarios]

