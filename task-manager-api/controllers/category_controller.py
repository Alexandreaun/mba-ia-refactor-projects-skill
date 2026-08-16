from flask import current_app

from database import db
from models.category import Category
from models.task import Task
from utils.errors import ApiError


class CategoryController:
    @staticmethod
    def list_categories():
        result = []
        for category in Category.query.all():
            data = category.to_dict()
            data['task_count'] = Task.query.filter_by(category_id=category.id).count()
            result.append(data)
        return result

    @staticmethod
    def create_category(data):
        if not data:
            raise ApiError('Dados inválidos', 400)

        name = data.get('name')
        if not name:
            raise ApiError('Nome é obrigatório', 400)

        category = Category()
        category.name = name
        category.description = data.get('description', '')
        category.color = data.get('color', '#000000')

        try:
            db.session.add(category)
            db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.exception('Erro ao criar categoria')
            raise ApiError('Erro ao criar categoria', 500)

        return category.to_dict()

    @staticmethod
    def update_category(category_id, data):
        category = Category.query.get(category_id)
        if not category:
            raise ApiError('Categoria não encontrada', 404)

        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        if 'color' in data:
            category.color = data['color']

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.exception('Erro ao atualizar categoria')
            raise ApiError('Erro ao atualizar', 500)

        return category.to_dict()

    @staticmethod
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            raise ApiError('Categoria não encontrada', 404)

        try:
            db.session.delete(category)
            db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.exception('Erro ao deletar categoria')
            raise ApiError('Erro ao deletar', 500)

        return {'message': 'Categoria deletada'}
