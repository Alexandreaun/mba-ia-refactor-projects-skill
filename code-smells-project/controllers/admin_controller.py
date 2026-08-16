import logging

from flask import jsonify

logger = logging.getLogger(__name__)


class AdminController:
    def __init__(self, admin_model, db_path):
        self.admin_model = admin_model
        self.db_path = db_path

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
        self.admin_model.reset_all()
        logger.warning("Banco de dados resetado via /admin/reset-db")
        return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200

    def health_check(self):
        try:
            counts = self.admin_model.get_counts()
            return jsonify({
                "status": "ok",
                "database": "connected",
                "counts": counts,
                "versao": "1.0.0",
                "ambiente": "producao",
                "db_path": self.db_path,
            }), 200
        except Exception:
            logger.exception("Falha no health check")
            return jsonify({"status": "erro", "detalhes": "Falha ao consultar o banco de dados"}), 500
