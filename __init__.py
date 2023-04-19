from flask import Flask
from api.index import app as api_app

def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_pyfile('config.py')

    flask_app.register_blueprint(api_app)

    return flask_app

if __name__ == "__main__":
    create_app().run()