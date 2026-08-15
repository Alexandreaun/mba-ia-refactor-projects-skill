from flask import current_app

from database import db
from models.task import Task
from models.user import User
from utils.errors import ApiError
from utils.helpers import MIN_PASSWORD_LENGTH, VALID_ROLES, validate_email


class UserController:
    @staticmethod
    def list_users():
        result = []
        for user in User.query.all():
            result.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'active': user.active,
                'created_at': str(user.created_at),
                'task_count': len(user.tasks),
            })
        return result

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ApiError('Usuário não encontrado', 404)

        data = user.to_dict()
        data['tasks'] = [task.to_dict() for task in Task.query.filter_by(user_id=user_id).all()]
        return data

    @staticmethod
    def create_user(data):
        if not data:
            raise ApiError('Dados inválidos', 400)

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not name:
            raise ApiError('Nome é obrigatório', 400)
        if not email:
            raise ApiError('Email é obrigatório', 400)
        if not password:
            raise ApiError('Senha é obrigatória', 400)

        if not validate_email(email):
            raise ApiError('Email inválido', 400)

        if len(password) < MIN_PASSWORD_LENGTH:
            raise ApiError('Senha deve ter no mínimo 4 caracteres', 400)

        if User.query.filter_by(email=email).first():
            raise ApiError('Email já cadastrado', 409)

        if role not in VALID_ROLES:
            raise ApiError('Role inválido', 400)

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.role = role

        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.exception('Erro ao criar usuário')
            raise ApiError('Erro ao criar usuário', 500)

        current_app.logger.info('Usuário criado: %s - %s', user.id, user.name)
        return user.to_dict()

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            raise ApiError('Usuário não encontrado', 404)
        if not data:
            raise ApiError('Dados inválidos', 400)

        if 'name' in data:
            user.name = data['name']

        if 'email' in data:
            if not validate_email(data['email']):
                raise ApiError('Email inválido', 400)

            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                raise ApiError('Email já cadastrado', 409)
            user.email = data['email']

        if 'password' in data:
            if len(data['password']) < MIN_PASSWORD_LENGTH:
                raise ApiError('Senha muito curta', 400)
            user.set_password(data['password'])

        if 'role' in data:
            if data['role'] not in VALID_ROLES:
                raise ApiError('Role inválido', 400)
            user.role = data['role']

        if 'active' in data:
            user.active = data['active']

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.exception('Erro ao atualizar usuário')
            raise ApiError('Erro ao atualizar', 500)

        return user.to_dict()

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ApiError('Usuário não encontrado', 404)

        for task in Task.query.filter_by(user_id=user_id).all():
            db.session.delete(task)

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.exception('Erro ao deletar usuário')
            raise ApiError('Erro ao deletar', 500)

        current_app.logger.info('Usuário deletado: %s', user_id)

    @staticmethod
    def get_user_tasks(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ApiError('Usuário não encontrado', 404)

        result = []
        for task in Task.query.filter_by(user_id=user_id).all():
            result.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'priority': task.priority,
                'created_at': str(task.created_at),
                'due_date': str(task.due_date) if task.due_date else None,
                'overdue': task.is_overdue(),
            })
        return result

    @staticmethod
    def login(data):
        if not data:
            raise ApiError('Dados inválidos', 400)

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise ApiError('Email e senha são obrigatórios', 400)

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise ApiError('Credenciais inválidas', 401)

        if not user.active:
            raise ApiError('Usuário inativo', 403)

        return {
            'message': 'Login realizado com sucesso',
            'user': user.to_dict(),
            'token': 'fake-jwt-token-' + str(user.id),
        }
