from flask_restx import fields


# -------------------------------
# Swagger Models (for API documentation only)
# -------------------------------
# These models define the expected input fields for Swagger UI and automatic validation
def swagger_auth_models(ns):
    """Swagger models for auth"""
    register_model = ns.model("Register", {
        "username": fields.String(required=True, default='sachin123',  description='e.g. sachin123'),   # Required username field
        "email": fields.String(required=True,default='sachin123@gmail.com',  description='e.g. sachin123@gmail.com'),      # Required email field
        "password": fields.String(required=True,default='sachin@123',  description='e.g. Sachin@123')    # Required password field
    })
    login_model = ns.model("Login", {
        "email": fields.String(required=True, default='sachin123@gmail.com',  description='e.g. sachin123@gmail.com'),      # Required email field
        "password": fields.String(required=True, default='sachin@123', description='e.g. Sachin@123')    # Required password field
    })
    return register_model, login_model
