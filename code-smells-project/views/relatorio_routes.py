from flask import Blueprint


def create_relatorio_blueprint(controller):
    bp = Blueprint("relatorios", __name__)
    bp.add_url_rule("/relatorios/vendas", "relatorio_vendas", controller.relatorio_vendas, methods=["GET"])
    return bp
