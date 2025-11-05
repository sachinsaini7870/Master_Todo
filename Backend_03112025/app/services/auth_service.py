from ..extensions import db  # SQLAlchemy instance for database operations
from ..models.user_model import User  # User model from SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  # For secure password hashing
from flask_jwt_extended import create_access_token  # To generate JWT access tokens
from datetime import timedelta  # To set token expiration time
from sqlalchemy.exc import OperationalError, SQLAlchemyError

# -------------------------------
# Register a new user
# -------------------------------
def register_user(data):
    """
    Handles user registration:
    1. Checks if username/email is unique
    2. Hashes the password
    3. Saves user to database
    4. Returns success message and user info
    """
    username = data["username"]  # Extract username from request data
    email = data["email"]        # Extract email
    password = data["password"]  # Extract password

    try:
        # -------------------------------
        # Check for uniqueness of username/email
        # -------------------------------
        # If a user already exists with the same username or email, return 400
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return {"error": "Username or email already exists"}, 400

        # -------------------------------
        # Hash the password
        # -------------------------------
        # Never store plain-text passwords
        hashed = generate_password_hash(password)

        # -------------------------------
        # Create new user and save to database
        # -------------------------------
        user = User(username=username, email=email, password_hash=hashed)
        db.session.add(user)    # Add new user to session
        db.session.commit()     # Commit to save in DB

        # -------------------------------
        # Return success response
        # -------------------------------
        return {"message": "User registered successfully", "user": user.to_dict()}, 201
    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError:
        db.session.rollback()
        return {"error": "Error saving user"}, 500
    
# -------------------------------
# Login an existing user
# -------------------------------
def login_user(data):
    """
    Handles user login:
    1. Verify email and password
    2. Generate JWT token if valid
    3. Return token and status
    """
    email = data["email"]      # Extract email
    password = data["password"]  # Extract password

    try:
        # -------------------------------
        # Fetch user by email
        # -------------------------------
        user = User.query.filter_by(email=email).first()

        # -------------------------------
        # Check credentials
        # -------------------------------
        # If user doesn't exist or password is incorrect, return 401
        if not user or not check_password_hash(user.password_hash, password):
            return {"error": "Invalid credentials"}, 401

        # -------------------------------
        # Generate JWT token
        # -------------------------------
        # identity should be a primitive type (int or str)
        # expires_delta sets token expiration (24 hours here)
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=24))

        # -------------------------------
        # Return access token
        # -------------------------------
        return {"access_token": token}, 200
    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError as err:
        return {"error": err.message}, 500