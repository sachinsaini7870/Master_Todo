# Backend_03112025\app\routes\todo.py
from flask_restx import Namespace, Resource # Flask-RESTX classes for namespaces, resources, and Swagger models
from flask import request  # To access incoming JSON payloads
from flask_jwt_extended import jwt_required, get_jwt_identity  # For JWT authentication
from marshmallow import ValidationError  # To catch validation errors from Marshmallow
from ..schemas.todo_schema import TodoCreateSchema, TodoUpdateSchema  # Marshmallow schemas for todo
from ..services.todo_service import (  # Service layer functions for CRUD operations
    create_todo_service, list_todos_service, get_todo_service,
    update_todo_service, delete_todo_service
)
from ..swagger_models.todo_models import swagger_todo_models

# -------------------------------
# Namespace definition
# -------------------------------
# Group all todo-related routes under this namespace
# Description is used in Swagger UI for clarity
todo_ns = Namespace("todos", description="Todo operations")

# Register Swagger models
todo_put_model, todo_post_model = swagger_todo_models(todo_ns)

# -------------------------------
# /todos route for list and create
# -------------------------------
@todo_ns.route("/")
class TodoList(Resource):
    @jwt_required()  # Require valid JWT to access
    def get(self):
        """
        GET /todos
        1. Get current user_id from JWT
        2. Call service layer to list todos for this user
        3. Return list of todos with proper HTTP status
        """
        user_id = int(get_jwt_identity())  # Extract current user ID from JWT
        # data, status = list_todos_service(user_id)  # Call service layer
        # return data, status
        return list_todos_service(user_id)

    @jwt_required()
    @todo_ns.expect(todo_post_model, validate=True)  # Validate incoming request against Swagger model
    def post(self):
        """
        POST /todos
        1. Validate input using Marshmallow schema
        2. If validation fails, return 400 with error messages
        3. Otherwise, create a new todo for the current user
        """
        try:
            data = TodoCreateSchema().load(request.json)  # Validate and deserialize request
        except ValidationError as err:
            return {"errors": err.messages}, 400  # Return validation errors
        user_id = int(get_jwt_identity())  # Get current user ID
        return create_todo_service(data, user_id)  # Call service layer to create todo

# -------------------------------
# /todos/<todo_id> route for individual todo
# -------------------------------
@todo_ns.route("/<int:todo_id>")
class TodoItem(Resource):
    @jwt_required()
    def get(self, todo_id):
        """
        GET /todos/<todo_id>
        1. Get the todo by ID for the current user
        2. Return formatted todo object
        """
        user_id = int(get_jwt_identity())
        return get_todo_service(todo_id, user_id)

    @jwt_required()
    @todo_ns.expect(todo_put_model)
    def put(self, todo_id):
        """
        PUT /todos/<todo_id>
        1. Validate input with Marshmallow schema (partial updates allowed)
        2. Update the todo for the current user
        """
        try:
            data = TodoUpdateSchema().load(request.json or {})  # Allow empty payload
        except ValidationError as err:
            return {"errors": err.messages}, 400
        user_id = int(get_jwt_identity())
        return update_todo_service(todo_id, data, user_id)

    @jwt_required()
    def delete(self, todo_id):
        """
        DELETE /todos/<todo_id>
        1. Delete the todo by ID for the current user
        2. Return success message or error
        """
        user_id = int(get_jwt_identity())
        return delete_todo_service(todo_id, user_id)
