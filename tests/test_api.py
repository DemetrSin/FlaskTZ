import unittest

from app import app
from models import Task, db


class TaskTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask application for testing
        app.config['TESTING'] = True
        app.config['MYSQL_DB'] = 'todo_d'  # Use the 'todo_d' database for tests
        self.app = app.test_client()  # Create a test client
        self.app.testing = True

        with app.app_context():
            # Create the tasks table if it doesn't exist and clear any existing data
            cursor = db.connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)"
            )
            cursor.execute("DELETE FROM tasks")  # Clear the tasks table
            db.connection.commit()
            cursor.close()

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            cursor = db.connection.cursor()
            cursor.execute("DROP TABLE tasks")  # Drop the tasks table
            db.connection.commit()
            cursor.close()

    def test_get_all_tasks(self):
        # Test the GET /tasks endpoint
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)  # Check if the response status is 200 OK
        self.assertEqual(response.get_json(), [])  # Check if the response data is an empty list

    def test_create_task(self):
        # Test the POST /tasks endpoint
        response = self.app.post('/tasks', json={'title': 'Test task', 'description': 'This is a test task'})
        self.assertEqual(response.status_code, 201)  # Check if the response status is 201 Created
        data = response.get_json()
        self.assertEqual(data['title'], 'Test task')  # Check if the title matches
        self.assertEqual(data['description'], 'This is a test task')  # Check if the description matches

    def test_get_task(self):
        # Test the GET /tasks/<task_id> endpoint
        self.app.post('/tasks', json={'title': 'Test task', 'description': 'This is a test task'})
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)  # Check if the response status is 200 OK
        data = response.get_json()
        self.assertEqual(data['title'], 'Test task')  # Check if the title matches
        self.assertEqual(data['description'], 'This is a test task')  # Check if the description matches

    def test_update_task(self):
        # Test the PUT /tasks/<task_id> endpoint
        self.app.post('/tasks', json={'title': 'Test task', 'description': 'This is a test task'})
        response = self.app.put('/tasks/1',
                                json={'title': 'Updated task', 'description': 'This is an updated test task'})
        self.assertEqual(response.status_code, 200)  # Check if the response status is 200 OK
        data = response.get_json()
        self.assertEqual(data['title'], 'Updated task')  # Check if the updated title matches
        self.assertEqual(data['description'],
                         'This is an updated test task')  # Check if the updated description matches

    def test_delete_task(self):
        # Test the DELETE /tasks/<task_id> endpoint
        self.app.post('/tasks', json={'title': 'Test task', 'description': 'This is a test task'})
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)  # Check if the response status is 200 OK
        self.assertEqual(response.get_json(),
                         {'message': 'Task deleted successfully'})  # Check if the deletion message matches

        # Verify that the task was deleted
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 404)  # Check if the response status is 404 Not Found
        self.assertEqual(response.get_json(), {'error': 'Task not found'})  # Check if the error message matches


if __name__ == '__main__':
    unittest.main()
