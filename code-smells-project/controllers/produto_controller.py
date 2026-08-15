from flask import request

from constants import CATEGORIAS_VALIDAS, NOME_PRODUTO_MAX_LENGTH, NOME_PRODUTO_MIN_LENGTH
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

        if not dados:
            return error("Dados inválidos", 400)
        if "nome" not in dados:
            return error("Nome é obrigatório", 400)
        if "preco" not in dados:
            return error("Preço é obrigatório", 400)
        if "estoque" not in dados:
            return error("Estoque é obrigatório", 400)

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0:
            return error("Preço não pode ser negativo", 400)
        if estoque < 0:
            return error("Estoque não pode ser negativo", 400)
        if len(nome) < NOME_PRODUTO_MIN_LENGTH:
            return error("Nome muito curto", 400)
        if len(nome) > NOME_PRODUTO_MAX_LENGTH:
            return error("Nome muito longo", 400)
        if categoria not in CATEGORIAS_VALIDAS:
            return error(f"Categoria inválida. Válidas: {CATEGORIAS_VALIDAS}", 400)

        produto_id = self.produto_model.criar(nome, descricao, preco, estoque, categoria)
        return success({"id": produto_id}, 201, mensagem="Produto criado")

    def atualizar_produto(self, produto_id):
        dados = request.get_json()

        produto_existente = self.produto_model.get_por_id(produto_id)
        if not produto_existente:
            return error("Produto não encontrado", 404)

        if not dados:
            return error("Dados inválidos", 400)
        if "nome" not in dados:
            return error("Nome é obrigatório", 400)
        if "preco" not in dados:
            return error("Preço é obrigatório", 400)
        if "estoque" not in dados:
            return error("Estoque é obrigatório", 400)

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0:
            return error("Preço não pode ser negativo", 400)
        if estoque < 0:
            return error("Estoque não pode ser negativo", 400)

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

        if preco_min:
            preco_min = float(preco_min)
        if preco_max:
            preco_max = float(preco_max)

        resultados = self.produto_model.buscar(termo, categoria, preco_min, preco_max)
        return success(resultados, total=len(resultados))
