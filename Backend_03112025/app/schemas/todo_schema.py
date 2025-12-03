# Backend_03112025\app\schemas\todo_schema.py
from marshmallow import Schema, fields, validate  # Schema base class, field types, and validators

# -------------------------------
# Schema for creating a new todo
# -------------------------------
class TodoCreateSchema(Schema):
    """
    Validates data when creating a new todo.
    Ensures required fields are present and correctly formatted.
    """
    title = fields.Str(
        required=True,                     # Title must be provided
        validate=validate.Length(min=1)    # At least 1 character long
    )
    description = fields.Str(required=False)
    completed = fields.Boolean()           # Optional field to mark todo as completed or not

# -------------------------------
# Schema for updating an existing todo
# -------------------------------
class TodoUpdateSchema(Schema):
    """
    Validates data when updating a todo.
    All fields are optional; only the provided fields are updated.
    """
    title = fields.Str(
        validate=validate.Length(min=1)    # If provided, title must have at least 1 character
    )
    description = fields.Str()
    completed = fields.Boolean()           # Optional field to mark todo as completed or not

# -------------------------------
# Schema for outputting todo data
# -------------------------------
class TodoOutSchema(Schema):
    """
    Defines how todo objects are serialized when sent in API responses.
    """
    id = fields.Int()                      # Todo ID
    title = fields.Str()                   # Todo title
    description = fields.Str()             # Todo description
    completed = fields.Bool()              # Completion status
    user_id = fields.Int()                 # ID of the user who owns this todo
