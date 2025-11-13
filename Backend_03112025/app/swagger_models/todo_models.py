# Backend_03112025\app\swagger_models\todo_models.py
from flask_restx import fields


# -------------------------------
# Swagger models for request/response documentation
# -------------------------------
# Model for creating/updating a todo (input from client)
def swagger_todo_models(ns):
    """Swagger models for todos"""
    todo_put_model = ns.model("TodoPut", {
        "title": fields.String(description='e.g. Learn flask_restx', default='Learn flask_restx'),               # Optional completed flag
        "description": fields.String(description='e.g. Learn flask_restx is very important.', default='Learn flask_restx is very important'),
        "completed": fields.Boolean(description='e.g. true/false', default=True)           # Optional completed flag
    })

    todo_post_model = ns.model("TodoPost", {
        "title": fields.String(required=True, description='e.g. Learn flask_restx', default='Learn flask_restx'),  # Title is required
        "description": fields.String(description='e.g. Learn flask_restx is very important.', default='Learn flask_restx is very important'),
        "completed": fields.Boolean(default=False, description='e.g. true/false')           # Optional completed flag
        
    })
    return todo_put_model, todo_post_model
