
from Models import Categoria, Estoque, Produtos, Fornecedor, Pessoa, Funcionario, Venda
from DAO import DaoCategoria, DaoVenda, DaoEstoque, DaoFornecedor, DaoPessoa, DaoFuncionario
from datetime import datetime

class ControllerCategoria:
    def cadastrarCategoria(self, novaCategoria):
        existe = False
        x = DaoCategoria.ler()
        for i in x:
            if i.categoria == novaCategoria:
                existe = True

        if not existe:
            DaoCategoria.salvar(novaCategoria)
            print('Categoria cadastrada com sucesso!')
        else:
            print('A categoria que deseja cadastrar já existe!')

    def removerCategoria(self, categoriaRemover):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoriaRemover, x))

        if not cat:
            print("A categoria que você deseja remover não existe.")
        else:
            for i in range(len(x)):
                if x[i].categoria == categoriaRemover:
                    del x[i]
                    break

            print("A categoria foi removida com sucesso!")
            #TODO: Colocar sem categoria no estoque.
            with open('categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')

    def alterarCategoria(self, categoriaAlterar, categoriaAlterada):
        x = DaoCategoria.ler()

        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))
        # Se a categoria a ser alterada já existe!
        if len(cat):
            cat1 = list(filter(lambda x: x.categoria == categoriaAlterada, x))
            # Se a categoria alterada não existe ainda.
            if len(cat1) == 0:
                x = list(map(lambda x: Categoria(categoriaAlterada) if x.categoria == categoriaAlterar else x, x))

                print("A alteração foi efetuada com sucesso!")
                #TODO: Alterar a categoria também do estoque.
            else:
                print("A categoria para a qual deseja alterar já existe!")
        else:
            print("A categoria que deseja alterar não existe!")

        with open("categoria.txt", "w") as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')


    def mostrarCategoria(self):
        categorias = DaoCategoria.ler()

        if len(categorias) == 0:
            print("Categoria vazia!")
        else:
            for i in categorias:
                print(f'Categoria: {i.categoria}')


# a = ControllerCategoria()
# a.cadastrarCategoria('Frios')

# a = ControllerCategoria()
# a.removerCategoria("Frutas")
# a.alterarCategoria("Carnes", "Verduras")
# a.mostrarCategoria()
