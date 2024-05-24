from flasgger import swag_from
from flask import request
from flask_restful import Resource

from models import Task


class TaskListResource(Resource):
    @swag_from('docs/tasks_get.yml')
    def get(self):
        tasks = Task.get_all_tasks()
        return tasks, 200

    @swag_from('docs/tasks_post.yml')
    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description', '')
        if not title:
            return {'error': 'Title is required'}, 400
        task = Task.create_task(title, description)
        return task, 201


class TaskResource(Resource):
    @swag_from('docs/task_get.yml')
    def get(self, task_id):
        task = Task.get_task(task_id)
        if not task:
            return {'error': 'Task not found'}, 404
        return task, 200

    @swag_from('docs/task_put.yml')
    def put(self, task_id):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        if not title and not description:
            return {'error': 'Nothing to update'}, 400
        task = Task.update_task(task_id, title, description)
        return task, 200

    @swag_from('docs/task_delete.yml')
    def delete(self, task_id):
        task = Task.get_task(task_id)
        if not task:
            return {'error': 'Task not found'}, 404
        Task.delete_task(task_id)
        return {'message': 'Task deleted successfully'}, 200
