from flask import request

from constants import CATEGORIA_PADRAO
from models.produto_model import ProdutoModel
from views.response import error, success


class ProdutoController:
    def __init__(self, produto_model):
        self.produto_model = produto_model

    def listar_produtos(self):
        produtos = self.produto_model.get_todos()
        return success(produtos)

    def buscar_produto(self, produto_id):
        produto = self.produto_model.get_por_id(produto_id)
        if produto:
            return success(produto)
        return error("Produto não encontrado", 404)

    def criar_produto(self):
        dados = request.get_json()

        erro = ProdutoModel.validar_dados(dados)
        if erro:
            return error(erro, 400)

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", CATEGORIA_PADRAO)

        produto_id = self.produto_model.criar(nome, descricao, preco, estoque, categoria)
        return success({"id": produto_id}, 201, mensagem="Produto criado")

    def atualizar_produto(self, produto_id):
        dados = request.get_json()

        produto_existente = self.produto_model.get_por_id(produto_id)
        if not produto_existente:
            return error("Produto não encontrado", 404)

        erro = ProdutoModel.validar_dados(dados)
        if erro:
            return error(erro, 400)

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", CATEGORIA_PADRAO)

        self.produto_model.atualizar(produto_id, nome, descricao, preco, estoque, categoria)
        return success(status=200, mensagem="Produto atualizado")

    def deletar_produto(self, produto_id):
        produto = self.produto_model.get_por_id(produto_id)
        if not produto:
            return error("Produto não encontrado", 404)

        self.produto_model.deletar(produto_id)
        return success(status=200, mensagem="Produto deletado")

    def buscar_produtos(self):
        termo = request.args.get("q", "")
        categoria = request.args.get("categoria", None)
        preco_min = request.args.get("preco_min", None)
        preco_max = request.args.get("preco_max", None)

        try:
            preco_min = float(preco_min) if preco_min else None
            preco_max = float(preco_max) if preco_max else None
        except ValueError:
            return error("preco_min e preco_max devem ser numéricos", 400)

        resultados = self.produto_model.buscar(termo, categoria, preco_min, preco_max)
        return success(resultados, total=len(resultados))
