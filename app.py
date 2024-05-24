from flask import Flask
from flask_restful import Api
from config import Config
from models import init_db
from resources.task import TaskListResource, TaskResource
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)
Swagger(app)

init_db(app)

api = Api(app)
api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/tasks/<int:task_id>')

if __name__ == '__main__':
    app.run(debug=True)
