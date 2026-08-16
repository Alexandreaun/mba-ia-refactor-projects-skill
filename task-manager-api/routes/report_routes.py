from flask import Blueprint, jsonify, request

from controllers.category_controller import CategoryController
from controllers.report_controller import ReportController

report_bp = Blueprint('reports', __name__)


@report_bp.route('/reports/summary', methods=['GET'])
def summary_report():
    return jsonify(ReportController.summary()), 200


@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
def user_report(user_id):
    return jsonify(ReportController.user_report(user_id)), 200


@report_bp.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(CategoryController.list_categories()), 200


@report_bp.route('/categories', methods=['POST'])
def create_category():
    return jsonify(CategoryController.create_category(request.get_json())), 201


@report_bp.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    return jsonify(CategoryController.update_category(cat_id, request.get_json())), 200


@report_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    return jsonify(CategoryController.delete_category(cat_id)), 200
