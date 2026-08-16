from flask import Blueprint, jsonify, request

from controllers.task_controller import TaskController

task_bp = Blueprint('tasks', __name__)


@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(TaskController.list_tasks()), 200


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    return jsonify(TaskController.get_task(task_id)), 200


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    return jsonify(TaskController.create_task(request.get_json())), 201


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    return jsonify(TaskController.update_task(task_id, request.get_json())), 200


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    TaskController.delete_task(task_id)
    return jsonify({'message': 'Task deletada com sucesso'}), 200


@task_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    return jsonify(TaskController.search(request.args)), 200


@task_bp.route('/tasks/stats', methods=['GET'])
def task_stats():
    return jsonify(TaskController.stats()), 200
