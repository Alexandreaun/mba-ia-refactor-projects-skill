import logging

from flask import jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        return jsonify({"erro": err.description, "sucesso": False}), err.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(err):
        logger.exception("Erro não tratado durante o processamento da requisição")
        return jsonify({"erro": "Erro interno no servidor", "sucesso": False}), 500
