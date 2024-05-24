from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from config import Config
from models import init_db
from resources.task import TaskListResource, TaskResource

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from Config class

# Initialize Swagger for API documentation
Swagger(app)

# Initialize the database with the Flask app
init_db(app)

# Initialize Flask-RESTful API
api = Api(app)

# Define API routes
api.add_resource(TaskListResource, '/tasks')  # Route for task list resource
api.add_resource(TaskResource, '/tasks/<int:task_id>')  # Route for single task resource

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
