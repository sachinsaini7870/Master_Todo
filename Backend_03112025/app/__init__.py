# Backend_03112025\app\__init__.py
from flask import Flask, jsonify
from .config import config_map
from .extensions import db, migrate, jwt, ma, api_bp, api, mail
from .errors import register_error_handlers
from .routes.auth import auth_ns
from .routes.todo import todo_ns
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy import text

def create_app(config_name="development"):
    app=Flask(__name__)

    # Add configurations to flask app from config file map with config_name
    app.config.from_object(config_map[config_name])
    
    # Add or Initialize extensions to app
    db.init_app(app) # add database extension to app
    migrate.init_app(app, db) # add sql migration with alembic to app
    jwt.init_app(app) # add jwt manager to app
    ma.init_app(app) # add Marshmallow validator to app
    mail.init_app(app)
    
    # Register namespaces in api
    api.init_app(api_bp) # add flask_restx api ui to app where route is /docs
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(todo_ns, path="/todos")
    
    # Register blueprint that contains restx namespaces
    app.register_blueprint(api_bp)
    
    # register error handlers
    register_error_handlers(app)
    
    # ✅ Health check endpoint for database status
    @app.route("/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"status": "ok", "database": "connected"}), 200
        except (OperationalError, SQLAlchemyError):
            return jsonify({"status": "error", "database": "down"}), 503
    
    @app.route("/")
    def home():
        return {"message":"this is home route"}

    
    return app

