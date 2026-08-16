import logging

from flask import Flask
from flask_cors import CORS

from config import Config
from controllers.admin_controller import AdminController
from controllers.pedido_controller import PedidoController
from controllers.produto_controller import ProdutoController
from controllers.relatorio_controller import RelatorioController
from controllers.usuario_controller import UsuarioController
from errors import register_error_handlers
from models.admin_model import AdminModel
from models.database import Database
from models.pedido_model import PedidoModel
from models.produto_model import ProdutoModel
from models.usuario_model import UsuarioModel
from views.admin_routes import create_admin_blueprint
from views.pedido_routes import create_pedido_blueprint
from views.produto_routes import create_produto_blueprint
from views.relatorio_routes import create_relatorio_blueprint
from views.usuario_routes import create_usuario_blueprint

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["DEBUG"] = Config.DEBUG
    CORS(app)

    db = Database(Config.DB_PATH)
    db.get_connection()

    produto_model = ProdutoModel(db)
    usuario_model = UsuarioModel(db)
    pedido_model = PedidoModel(db)
    admin_model = AdminModel(db)

    produto_controller = ProdutoController(produto_model)
    usuario_controller = UsuarioController(usuario_model)
    pedido_controller = PedidoController(pedido_model)
    relatorio_controller = RelatorioController(pedido_model)
    admin_controller = AdminController(admin_model, db.db_path)

    app.register_blueprint(create_produto_blueprint(produto_controller))
    app.register_blueprint(create_usuario_blueprint(usuario_controller))
    app.register_blueprint(create_pedido_blueprint(pedido_controller))
    app.register_blueprint(create_relatorio_blueprint(relatorio_controller))
    app.register_blueprint(create_admin_blueprint(admin_controller))

    register_error_handlers(app)

    return app


app = create_app()

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("SERVIDOR INICIADO")
    logger.info("Rodando em http://localhost:%s", Config.PORT)
    logger.info("=" * 50)
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
