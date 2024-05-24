from flask_mysqldb import MySQL
from datetime import datetime

db = MySQL()


def init_db(app):
    db.init_app(app)


class Task:
    @staticmethod
    def get_all_tasks():
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        cursor.close()
        for task in tasks:
            task['created_at'] = task['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            task['updated_at'] = task['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        return tasks

    @staticmethod
    def get_task(task_id):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        cursor.close()
        if task:
            task['created_at'] = task['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            task['updated_at'] = task['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        return task

    @staticmethod
    def create_task(title, description):
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
        db.connection.commit()
        task_id = cursor.lastrowid
        cursor.close()
        return Task.get_task(task_id)

    @staticmethod
    def update_task(task_id, title, description):
        cursor = db.connection.cursor()
        cursor.execute("UPDATE tasks SET title = %s, description = %s WHERE id = %s", (title, description, task_id))
        db.connection.commit()
        cursor.close()
        return Task.get_task(task_id)

    @staticmethod
    def delete_task(task_id):
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        db.connection.commit()
        cursor.close()
        return {'message': 'Task deleted successfully'}
