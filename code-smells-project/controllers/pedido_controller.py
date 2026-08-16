from flask import request

from constants import STATUS_PEDIDO_VALIDOS
from services.notification_service import notificar_mudanca_status, notificar_pedido_criado
from views.response import error, success


class PedidoController:
    def __init__(self, pedido_model):
        self.pedido_model = pedido_model

    def criar_pedido(self):
        dados = request.get_json()

        if not dados:
            return error("Dados inválidos", 400)

        usuario_id = dados.get("usuario_id")
        itens = dados.get("itens", [])

        if not usuario_id:
            return error("Usuario ID é obrigatório", 400)
        if not itens:
            return error("Pedido deve ter pelo menos 1 item", 400)

        resultado = self.pedido_model.criar(usuario_id, itens)
        if "erro" in resultado:
            return error(resultado["erro"], 400)

        notificar_pedido_criado(resultado["pedido_id"], usuario_id)

        return success(resultado, 201, mensagem="Pedido criado com sucesso")

    def listar_pedidos_usuario(self, usuario_id):
        pedidos = self.pedido_model.get_por_usuario(usuario_id)
        return success(pedidos)

    def listar_todos_pedidos(self):
        pedidos = self.pedido_model.get_todos()
        return success(pedidos)

    def atualizar_status_pedido(self, pedido_id):
        dados = request.get_json()
        novo_status = dados.get("status", "")

        if novo_status not in STATUS_PEDIDO_VALIDOS:
            return error("Status inválido", 400)

        self.pedido_model.atualizar_status(pedido_id, novo_status)
        notificar_mudanca_status(pedido_id, novo_status)

        return success(status=200, mensagem="Status atualizado")
