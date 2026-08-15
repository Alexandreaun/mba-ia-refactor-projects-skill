import datetime

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from config import settings
from database import db
from routes.task_routes import task_bp
from routes.user_routes import user_bp
from routes.report_routes import report_bp
from utils.errors import ApiError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = settings.SECRET_KEY

CORS(app)
db.init_app(app)

app.register_blueprint(task_bp)
app.register_blueprint(user_bp)
app.register_blueprint(report_bp)


@app.errorhandler(ApiError)
def handle_api_error(error):
    return jsonify(error.payload), error.status_code


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    if isinstance(error, HTTPException):
        return error
    app.logger.exception('Erro não tratado')
    return jsonify({'error': 'Erro interno'}), 500


@app.route('/health')
def health():
    return {'status': 'ok', 'timestamp': str(datetime.datetime.now())}

@app.route('/')
def index():
    return {'message': 'Task Manager API', 'version': '1.0'}

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5051)
