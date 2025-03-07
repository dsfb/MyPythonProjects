
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
            #TODO: Colocar os produtos desta categoria como sem categoria no estoque.
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
                #TODO: Alterar a categoria também dos produtos desta categoria no estoque.
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


class ControllerEstoque:
    def cadastrarProduto(self, nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda x: x.categoria == categoria, y))
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if h:
            if not est:
                produto = Produtos(nome, preco, categoria)
                DaoEstoque.salvar(produto, quantidade)
                print("Produto cadastrado com sucesso!")
            else:
                print("Erro: Produto já existe em estoque!")
        else:
            print("Erro: Categoria inexistente!")

    def removerProduto(self, nome):
        x = DaoEstoque.ler()
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if est:
            for i in range(len(x)):
                if x[i].produto.nome == nome:
                    del x[i]
                    print('O produto foi removido com sucesso!')
                    break
        else:
            print("Erro: o produto que você deseja remover, não existe!")

        with open('estoque.txt', 'w') as arg:
            for i in x:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                    i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines("\n")

    def alterarProduto(self, nomeParaAlterar, novoNome, novoPreco, novaCategoria, novaQuantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()

        h = list(filter(lambda x: x.categoria == novaCategoria, y))
        if h:
            est = list(filter(lambda x: x.produto.nome == nomeParaAlterar, x))
            if est:
                est2 = list(filter(lambda x: x.produto.nome == novoNome, x))
                if not est2:
                    x = list(map(lambda x: Estoque(Produtos(novoNome, novoPreco, novaCategoria), novaQuantidade)
                        if (x.produto.nome == nomeParaAlterar) else x, x))
                    print("O produto foi alterado  com sucesso!")
                else:
                    print("Erro: O produto já está cadastrado!")
            else:
                print("Erro: O produto que você deseja alterar não existe!")

            with open('estoque.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                        i.produto.categoria + "|" + str(i.quantidade))
                    arq.writelines("\n")
        else:
            print("Erro: A categoria informada não existe!")

    def mostrarEstoque(self):
        estoque = DaoEstoque.ler()

        if not estoque:
            print("Erro: o estoque está vazio!")
        else:
            print("==========Produtos==========")
            for i in estoque:                
                print(f"Nome: {i.produto.nome}\n"
                    f"Preço: {i.produto.preco}\n"
                    f"Categoria: {i.produto.categoria}\n"
                    f"Quantidade: {i.quantidade}"
                )
                print("--------------------")

a = ControllerEstoque()
# a.cadastrarProduto("banana", "5", "Verduras", 10) # Banana não é uma verdura!
# a.removerProduto('banana')
# a.alterarProduto('banana', 'maca', '5', 'Verduras', '20')
a.mostrarEstoque()
