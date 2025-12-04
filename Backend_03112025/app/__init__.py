# Backend_03112025\app\__init__.py
from flask import Flask
from .config import config_map
from .extensions import db, migrate, jwt, ma, api_bp, api, mail, cors
from .errors import register_error_handlers
from .routes.auth import auth_ns
from .routes.todo import todo_ns
from .routes.home import home_bp

def create_app(config_name="development"):
    app=Flask(__name__)

    # Add configurations to flask app from config file map with config_name
    app.config.from_object(config_map[config_name])
    
    # Add or Initialize extensions to app
    db.init_app(app)                # add database extension to app
    migrate.init_app(app, db)       # add sql migration with alembic to app
    jwt.init_app(app)               # add jwt manager to app
    ma.init_app(app)                # add Marshmallow validator to app
    mail.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"} })
    
    
    # ----------------------------
    # Setup Flask-RESTX API ROUTES
    # ----------------------------
    api.init_app(api_bp)
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(todo_ns, path="/todos")


    # Register blueprints
    app.register_blueprint(home_bp)   # / and /health
    app.register_blueprint(api_bp)    # /api/auth , /api/todos
    
    
    # register error handlers
    register_error_handlers(app)
    
    
    return app

