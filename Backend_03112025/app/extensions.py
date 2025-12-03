# Backend_03112025\app\extensions.py
from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS


db = SQLAlchemy()
migrate= Migrate()
jwt=JWTManager()
ma=Marshmallow()
mail = Mail()
cors = CORS()


# configure Bearer Auth
authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
    }
}


api=Api(
    title="Todo API",
    version="1.0",
    description="Production-grade Todo API",
    authorizations=authorizations,
    security="Bearer Auth",
    doc="/docs"  # Swagger UI at /api/docs (see blueprint url_prefix)
)


# Blueprint for all APIs
api_bp = Blueprint("api", __name__, url_prefix="/api")



