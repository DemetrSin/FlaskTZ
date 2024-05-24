from flask_mysqldb import MySQL

# Initialize MySQL instance
db = MySQL()


def init_db(app):
    """
    Initialize the database with the given Flask app.

    Args:
        app (Flask): The Flask application instance.
    """
    db.init_app(app)


class Task:
    @staticmethod
    def get_all_tasks():
        """
        Retrieve all tasks from the database.

        Returns:
            list: A list of dictionaries representing all tasks.
        """
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        cursor.close()
        for task in tasks:
            # Format the created_at and updated_at fields
            task['created_at'] = task['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            task['updated_at'] = task['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        return tasks

    @staticmethod
    def get_task(task_id):
        """
        Retrieve a single task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            dict: A dictionary representing the task, or None if not found.
        """
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        cursor.close()
        if task:
            # Format the created_at and updated_at fields
            task['created_at'] = task['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            task['updated_at'] = task['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        return task

    @staticmethod
    def create_task(title, description):
        """
        Create a new task in the database.

        Args:
            title (str): The title of the task.
            description (str): The description of the task.

        Returns:
            dict: A dictionary representing the created task.
        """
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
        db.connection.commit()
        task_id = cursor.lastrowid
        cursor.close()
        return Task.get_task(task_id)

    @staticmethod
    def update_task(task_id, title, description):
        """
        Update an existing task in the database.

        Args:
            task_id (int): The ID of the task to update.
            title (str): The new title of the task.
            description (str): The new description of the task.

        Returns:
            dict: A dictionary representing the updated task.
        """
        cursor = db.connection.cursor()
        cursor.execute("UPDATE tasks SET title = %s, description = %s WHERE id = %s", (title, description, task_id))
        db.connection.commit()
        cursor.close()
        return Task.get_task(task_id)

    @staticmethod
    def delete_task(task_id):
        """
        Delete a task from the database.

        Args:
            task_id (int): The ID of the task to delete.

        Returns:
            dict: A dictionary with a message indicating successful deletion.
        """
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        db.connection.commit()
        cursor.close()
        return {'message': 'Task deleted successfully'}
