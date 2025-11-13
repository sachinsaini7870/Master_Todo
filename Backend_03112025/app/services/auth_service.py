# Backend_03112025\app\services\auth_service.py
from ..extensions import db  # SQLAlchemy instance for database operations
from ..models.user_model import User  # User model from SQLAlchemy
from ..models.otp_model import OTP
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)  # For secure password hashing
from flask_jwt_extended import create_access_token  # To generate JWT access tokens
from datetime import datetime, timedelta  # To set token expiration time
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from ..utils.otp_generator import generate_otp
from ..utils.send_email import send_otp_email


def register_user(data):
    username = data["username"].strip()
    email = data["email"].strip().lower()
    password = data["password"]

    try:
        # Check duplicates
        if User.query.filter(
            (User.username == username) & (User.email == email)
        ).first():
            return {"error": "Username or email already exists"}, 400

        # Hash password
        hashed = generate_password_hash(password)

        # Create user with pending status
        user = User(
            username=username,
            email=email,
            password_hash=hashed,
            status="pending",
            email_verified=False,
        )
        db.session.add(user)
        db.session.commit()

        # Generate OTP
        otp_code = generate_otp()

        otp_entry = OTP(
            user_id=user.id,
            otp=otp_code,
            purpose="register",
            channel="email",
            attempt_count=1,
            expires_at=datetime.utcnow() + timedelta(minutes=5),
        )
        db.session.add(otp_entry)
        db.session.commit()

        send_otp_email(user.email, otp_code)

        return {
            "message": "Registration successful, verify OTP",
            # "otp": otp_code,  # development only
            "user_id": user.id,
        }, 201

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
    email = data["email"]  # Extract email
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
        user_dict = user.to_dict()
        additional_claims = {
            "username": user_dict["username"],
            "email": user_dict["email"],
            "email_verified": user_dict["email_verified"],
            "status": user_dict["status"],
            "created_at": user_dict["created_at"],
            "updated_at": user_dict["updated_at"],
        }

        token = create_access_token(
            identity=str(user.id), fresh=True, additional_claims=additional_claims
        )

        # -------------------------------
        # Return access token
        # -------------------------------
        return {"access_token": token}, 200
    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError as err:
        return {"error": err.message}, 500


def reset_password_service(data):
    email = data["email"]
    new_password = data["new_password"]

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 404

        # ✅ Hash new password securely
        hashed_password = generate_password_hash(new_password)
        user.password_hash = hashed_password
        db.session.commit()

        return {"message": "Password reset successfully"}, 200
    except OperationalError:
        return {"error": "Database not reachable"}, 503

    except Exception as e:
        db.session.rollback()
        print(f"Error resetting password: {e}")
        return {"error": "Error resetting password"}, 500
