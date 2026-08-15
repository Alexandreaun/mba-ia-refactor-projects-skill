from datetime import datetime, timedelta

from models.category import Category
from models.task import Task
from models.user import User
from utils.errors import ApiError
from utils.helpers import calculate_percentage


class ReportController:
    @staticmethod
    def summary():
        total_tasks = Task.query.count()
        total_users = User.query.count()
        total_categories = Category.query.count()

        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()

        priority_counts = {p: Task.query.filter_by(priority=p).count() for p in range(1, 6)}

        all_tasks = Task.query.all()

        overdue_list = [
            {
                'id': task.id,
                'title': task.title,
                'due_date': str(task.due_date),
                'days_overdue': (datetime.utcnow() - task.due_date).days,
            }
            for task in all_tasks if task.is_overdue()
        ]

        tasks_by_user = {}
        for task in all_tasks:
            tasks_by_user.setdefault(task.user_id, []).append(task)

        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_tasks = Task.query.filter(Task.created_at >= seven_days_ago).count()
        recent_done = Task.query.filter(
            Task.status == 'done',
            Task.updated_at >= seven_days_ago
        ).count()

        user_stats = []
        for user in User.query.all():
            user_tasks = tasks_by_user.get(user.id, [])
            completed = sum(1 for task in user_tasks if task.status == 'done')
            user_stats.append({
                'user_id': user.id,
                'user_name': user.name,
                'total_tasks': len(user_tasks),
                'completed_tasks': completed,
                'completion_rate': calculate_percentage(completed, len(user_tasks)),
            })

        return {
            'generated_at': str(datetime.utcnow()),
            'overview': {
                'total_tasks': total_tasks,
                'total_users': total_users,
                'total_categories': total_categories,
            },
            'tasks_by_status': {
                'pending': pending,
                'in_progress': in_progress,
                'done': done,
                'cancelled': cancelled,
            },
            'tasks_by_priority': {
                'critical': priority_counts[1],
                'high': priority_counts[2],
                'medium': priority_counts[3],
                'low': priority_counts[4],
                'minimal': priority_counts[5],
            },
            'overdue': {
                'count': len(overdue_list),
                'tasks': overdue_list,
            },
            'recent_activity': {
                'tasks_created_last_7_days': recent_tasks,
                'tasks_completed_last_7_days': recent_done,
            },
            'user_productivity': user_stats,
        }

    @staticmethod
    def user_report(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ApiError('Usuário não encontrado', 404)

        tasks = Task.query.filter_by(user_id=user_id).all()
        total = len(tasks)
        done = sum(1 for task in tasks if task.status == 'done')
        pending = sum(1 for task in tasks if task.status == 'pending')
        in_progress = sum(1 for task in tasks if task.status == 'in_progress')
        cancelled = sum(1 for task in tasks if task.status == 'cancelled')
        high_priority = sum(1 for task in tasks if task.priority <= 2)
        overdue = sum(1 for task in tasks if task.is_overdue())

        return {
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            },
            'statistics': {
                'total_tasks': total,
                'done': done,
                'pending': pending,
                'in_progress': in_progress,
                'cancelled': cancelled,
                'overdue': overdue,
                'high_priority': high_priority,
                'completion_rate': calculate_percentage(done, total),
            }
        }
