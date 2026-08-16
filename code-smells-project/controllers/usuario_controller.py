from flask import request

from views.response import error, success


class UsuarioController:
    def __init__(self, usuario_model):
        self.usuario_model = usuario_model

    def listar_usuarios(self):
        usuarios = self.usuario_model.get_todos()
        return success(usuarios)

    def buscar_usuario(self, usuario_id):
        usuario = self.usuario_model.get_por_id(usuario_id)
        if usuario:
            return success(usuario)
        return error("Usuário não encontrado", 404)

    def criar_usuario(self):
        dados = request.get_json()

        if not dados:
            return error("Dados inválidos", 400)

        nome = dados.get("nome", "")
        email = dados.get("email", "")
        senha = dados.get("senha", "")

        if not nome or not email or not senha:
            return error("Nome, email e senha são obrigatórios", 400)

        usuario_id = self.usuario_model.criar(nome, email, senha)
        return success({"id": usuario_id}, 201)

    def login(self):
        dados = request.get_json()
        email = dados.get("email", "")
        senha = dados.get("senha", "")

        if not email or not senha:
            return error("Email e senha são obrigatórios", 400)

        usuario = self.usuario_model.login(email, senha)
        if usuario:
            return success(usuario, mensagem="Login OK")
        return error("Email ou senha inválidos", 401)
