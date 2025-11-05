from flask_restx import Namespace, Resource  # For creating namespaces, RESTful resources, and Swagger models
from flask import request  # To access incoming JSON payloads
from marshmallow import ValidationError  # To handle validation errors from Marshmallow schemas
from ..schemas.auth_schema import RegisterSchema, LoginSchema  # Marshmallow schemas for validating register/login input
from ..services.auth_service import register_user, login_user  # Service layer functions for user registration and login
from ..swagger_models.auth_models import swagger_auth_models

# Create a Namespace for authentication routes
# This groups related routes together and adds descriptions for Swagger docs
auth_ns = Namespace("auth", description="Authentication operations")


# Register Swagger models
register_model, login_model = swagger_auth_models(auth_ns)


# -------------------------------
# /register Route
# -------------------------------
@auth_ns.route("/register")
class Register(Resource):
    # Expect the register_model for Swagger documentation and validate automatically
    @auth_ns.expect(register_model, validate=True)
    def post(self):
        """
        POST /auth/register
        1. Validate incoming JSON using Marshmallow schema
        2. If validation fails, return 400 with error messages
        3. Otherwise, call service function to register user
        """
        try:
            # Load and validate incoming JSON data
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            # Return validation errors with HTTP 400
            return {"errors": err.messages}, 400
        # Call the service layer to register the user
        return register_user(data)

# -------------------------------
# /login Route
# -------------------------------
@auth_ns.route("/login")
class Login(Resource):
    # Expect the login_model for Swagger documentation and validate automatically
    @auth_ns.expect(login_model, validate=True)
    def post(self):
        """
        POST /auth/login
        1. Validate incoming JSON using Marshmallow schema
        2. If validation fails, return 400 with error messages
        3. Otherwise, call service function to login user
        """
        try:
            # Load and validate incoming JSON data
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            # Return validation errors with HTTP 400
            return {"errors": err.messages}, 400
        # Call the service layer to log in the user and return token or response
        return login_user(data)
