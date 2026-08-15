import logging

from flask import jsonify

logger = logging.getLogger(__name__)


class AdminController:
    def __init__(self, db):
        self.db = db

    def index(self):
        return jsonify({
            "mensagem": "Bem-vindo à API da Loja",
            "versao": "1.0.0",
            "endpoints": {
                "produtos": "/produtos",
                "usuarios": "/usuarios",
                "pedidos": "/pedidos",
                "login": "/login",
                "relatorios": "/relatorios/vendas",
                "health": "/health",
            },
        })

    def reset_database(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM itens_pedido")
        cursor.execute("DELETE FROM pedidos")
        cursor.execute("DELETE FROM produtos")
        cursor.execute("DELETE FROM usuarios")
        conn.commit()
        logger.warning("Banco de dados resetado via /admin/reset-db")
        return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200

    def health_check(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.execute("SELECT COUNT(*) FROM produtos")
            produtos = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            usuarios = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM pedidos")
            pedidos = cursor.fetchone()[0]

            return jsonify({
                "status": "ok",
                "database": "connected",
                "counts": {
                    "produtos": produtos,
                    "usuarios": usuarios,
                    "pedidos": pedidos,
                },
                "versao": "1.0.0",
                "ambiente": "producao",
                "db_path": self.db.db_path,
            }), 200
        except Exception:
            logger.exception("Falha no health check")
            return jsonify({"status": "erro", "detalhes": "Falha ao consultar o banco de dados"}), 500
