# Backend_03112025\app\schemas\auth_schema.py
from marshmallow import Schema, fields, validate  # Schema base class, field types, and validators

# -------------------------------
# Schema for user registration
# -------------------------------
class RegisterSchema(Schema):
    """
    Marshmallow schema to validate incoming registration data.
    Ensures proper types and basic rules for each field.
    """
    username = fields.Str(
        required=True,                      # Must be provided
        validate=validate.Length(min=3)     # Minimum 3 characters long
    )
    email = fields.Email(
        required=True                       # Must be provided and a valid email format
    )
    password = fields.Str(
        required=True,                      # Must be provided
        validate=validate.Length(min=6)     # Minimum 6 characters for security
    )

# -------------------------------
# Schema for user login
# -------------------------------
class LoginSchema(Schema):
    """
    Marshmallow schema to validate login data.
    Only requires email and password.
    """
    email = fields.Email(
        required=True                       # Must be provided and a valid email
    )
    password = fields.Str(
        required=True                       # Must be provided
    )

class ResetPasswordSchema(Schema):
    email = fields.Email(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=6))