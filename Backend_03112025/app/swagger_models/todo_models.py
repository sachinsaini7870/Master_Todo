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
    todo_out_model = ns.model("TodoOut", {
        "id": fields.Integer(description='It show integer value with your todo post as id e.g. 1, 2, 3, etc'),                 # Todo ID
        "title": fields.String(description='It show String todo title e.g. Learn flask_restx'),               # Todo title
        "description": fields.String(description='e.g. Learn flask_restx is very important.'),
        "completed": fields.Boolean(description='It show boolean value true/false'),          # Completed flag
        "user_id": fields.Integer(description='It show integer value with your todo user as id e.g. 1, 2, 3, etc')             # ID of user who owns the todo
    })
    todo_post_model = ns.model("TodoPost", {
        "title": fields.String(required=True, description='e.g. Learn flask_restx', default='Learn flask_restx'),  # Title is required
        "description": fields.String(description='e.g. Learn flask_restx is very important.', default='Learn flask_restx is very important'),
        "completed": fields.Boolean(default=False, description='e.g. true/false')           # Optional completed flag
        
    })
    return todo_put_model, todo_out_model, todo_post_model
