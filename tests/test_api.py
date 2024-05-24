import unittest
from app import app, db


class TaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.connection.cursor().execute("DELETE FROM tasks")

    def test_create_task(self):
        response = self.app.post('/tasks', json={'title': 'Test task'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], 'Test task')


if __name__ == '__main__':
    unittest.main()
