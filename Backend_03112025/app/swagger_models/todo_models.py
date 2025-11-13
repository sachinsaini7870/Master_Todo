# Backend_03112025\app\swagger_models\todo_models.py
from flask_restx import fields


# -------------------------------
# Swagger models for request/response documentation
# -------------------------------
# Model for creating/updating a todo (input from client)
def swagger_todo_in_models(ns):
    """Swagger input models for todos"""
    todo_put_in_model = ns.model(
        "TodoPutIn",
        {
            "title": fields.String(
                description="e.g. Learn flask_restx", default="Learn flask_restx"
            ),  # Optional completed flag
            "description": fields.String(
                description="e.g. Learn flask_restx is very important.",
                default="Learn flask_restx is very important",
            ),
            "completed": fields.Boolean(
                description="e.g. true/false", default=True
            ),  # Optional completed flag
        },
    )

    todo_post_in_model = ns.model(
        "TodoPostIn",
        {
            "title": fields.String(
                required=True,
                description="e.g. Learn flask_restx",
                default="Learn flask_restx",
            ),  # Title is required
            "description": fields.String(
                description="e.g. Learn flask_restx is very important.",
                default="Learn flask_restx is very important",
            ),
            "completed": fields.Boolean(
                default=False, description="e.g. true/false"
            ),  # Optional completed flag
        },
    )

    return todo_post_in_model, todo_put_in_model


def swagger_todo_out_models(ns):
    """Swagger output models for todos"""

    todo_post_out_model = ns.model(
        "TodoPostOut",
        {
            "id": fields.Integer(description="Id of todo app"),
            "title": fields.String(description="e.g. Learn flask_restx"),
            "description": fields.String(
                description="e.g. Learn flask_restx is very important."
            ),
            "completed": fields.Boolean(description="e.g. true/false"),
            "created_at": fields.String(description="todo created time"),
            "updated_at": fields.String(description="todo updated time"),
        },
    )

    todo_put_out_model = ns.model(
        "TodoPutOut",
        {
            "id": fields.Integer(description="Id of todo app"),
            "title": fields.String(description="e.g. Learn flask_restx"),
            "description": fields.String(
                description="e.g. Learn flask_restx is very important."
            ),
            "completed": fields.Boolean(description="e.g. true/false"),
            "created_at": fields.String(description="todo created time"),
            "updated_at": fields.String(description="todo updated time"),
        },
    )

    return todo_post_out_model, todo_put_out_model
