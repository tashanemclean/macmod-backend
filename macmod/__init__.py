import os

from flask import Flask

from flask_mongoengine import MongoEngine

from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv('.env')

db = MongoEngine()

def create_app(app_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"*": {"origins": "*"}}) # the only one domain with access
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    dbhost = os.environ.get("DATABASE_HOST")
    dbusername = os.environ.get("DATABASE_USERNAME")
    dbpassword = os.environ.get("DATABASE_PASSWORD")

    app.config.from_mapping(
        JWT_SECRET_KEY=os.environ.get("SECRET_KEY"),
        TESTING=True,
        debug=True,
        MONGODB_SETTINGS={
            'host': dbhost,
            'username': dbusername,
            'password': dbpassword
        }
    )

    if app_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(app_config)

    db.init_app(app)

    from macmod import main, user
    app.register_blueprint(main.main)
    app.register_blueprint(main.menu)
    app.register_blueprint(main.shop)
    app.register_blueprint(user.user)

    return app
app = create_app()