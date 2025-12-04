# Backend_03112025\app\services\auth_service.py
from ..extensions import db
from ..models.auth_models import USER, OTP, FORGOT_PASSWORD
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from ..utils.otp_generator import generate_otp
from ..utils.send_email import send_otp_email, send_link_email
import os


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
        user = USER.query.filter_by(email=email).first()

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
            identity=str(user.id),
            fresh=True,
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=24),
        )

        # -------------------------------
        # Return access token
        # -------------------------------
        return {"token": token, "user": additional_claims["username"]}, 200
    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError as err:
        return {"error": err.message}, 500


def register_user(data):
    username = data["username"].strip()
    email = data["email"].strip().lower()
    password = data["password"]

    try:
        # Check duplicates
        if USER.query.filter(
            (USER.username == username) & (USER.email == email)
        ).first():
            return {"error": "USERname or email already exists"}, 400

        # Hash password
        hashed = generate_password_hash(password)

        # Create user with pending status
        user = USER(
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
            "user_id": user.id,
            "user_email": user.email,
        }, 201

    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError:
        db.session.rollback()
        return {"error": "Error saving user"}, 500


def resend_register_otp_service(data):
    email = data["email"]
    purpose = "register"

    try:
        # Fetch user
        user = USER.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 404

        # User must still be pending
        if user.status != "pending":
            return {"error": "User already registered"}, 400

        # Count today's OTP generation
        today_start = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        count_today = OTP.query.filter(
            OTP.user_id == user.id,
            OTP.purpose == purpose,
            OTP.created_at >= today_start,
        ).count()

        if count_today >= 5:
            return {"error": "Max OTP limit reached for today. Try tomorrow."}, 429

        # Mark previous OTP as used
        last_otp = (
            OTP.query.filter_by(user_id=user.id, purpose=purpose, is_used=False)
            .order_by(OTP.created_at.desc())
            .first()
        )

        if last_otp:
            last_otp.is_used = True
            db.session.commit()

        # Generate new OTP
        new_otp_code = generate_otp()

        new_otp = OTP(
            user_id=user.id,
            otp=new_otp_code,
            purpose=purpose,
            channel="email",
            expires_at=datetime.utcnow() + timedelta(minutes=5),
            attempt_count=last_otp.attempt_count + 1,
        )

        db.session.add(new_otp)
        db.session.commit()

        send_otp_email(user.email, new_otp_code)

        return {
            "message": "OTP resent successfully",
            # "otp": new_otp_code,  # development only
            "user_id": user.id,
            "user_email": user.email,
            "attempts_today": count_today + 1,
        }, 200

    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError:
        db.session.rollback()
        return {"error": "Error processing OTP"}, 500


def verify_register_otp_service(data):
    email = data.get("email")
    entered_otp = data["otp"]
    purpose = "register"

    try:
        # Fetch user
        user = USER.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 404

        # User must be pending
        if user.status != "pending":
            return {"error": "User already verified or invalid status"}, 400

        # Fetch latest OTP
        otp_obj = (
            OTP.query.filter_by(user_id=user.id, purpose=purpose, is_used=False)
            .order_by(OTP.created_at.desc())
            .first()
        )

        if not otp_obj:
            return {"error": "No OTP found"}, 404

        # Check expiry
        if datetime.utcnow() > otp_obj.expires_at:
            return {"error": "OTP expired"}, 400

        # Check OTP
        if otp_obj.otp != entered_otp:
            otp_obj.attempt_count += 1
            db.session.commit()
            return {"error": "Invalid OTP"}, 400

        # Mark OTP used
        otp_obj.is_used = True

        # Update user status
        user.status = "active"
        user.email_verified = True

        db.session.commit()

        # Generate JWT directly
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
            identity=str(user.id),
            fresh=True,
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=24),
        )


        return {
            "message": "OTP verified successfully",
            "token": token,
            "username": user.username,
        }, 200

    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError as err:
        db.session.rollback()
        return {"error": "Database error", "err": err}, 500


def forgot_service(data):
    email = data["email"]

    try:
        user = USER.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 404

        if user.status != "active":
            return {"error": "Inactive user"}, 400

        # Genrate jwt token
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
            identity=str(user.id),
            fresh=True,
            additional_claims=additional_claims,
            expires_delta=timedelta(minutes=5),
        )

        
        forgot_entry = FORGOT_PASSWORD(
            user_id=user.id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(minutes=5),
        )

        db.session.add(forgot_entry)
        db.session.commit()

        resetPasswordLink = (
            os.getenv("REACT_APP_FRONT_URL") + "/auth/reset-password/" + token
        )

        send_link_email(user.email, resetPasswordLink)

        return {
            "message": "Forgot link sent",
            "user_email": user.email,
            "user_id": user.id,
        }, 200

    except Exception as err:
        db.session.rollback()
        return {"error": str(err)}, 500


def reset_password_service(data):
    token = data["token"]
    new_password = data["password"]

    try:
        reset_entry = (
            FORGOT_PASSWORD.query.filter_by(token=token)
            .order_by(FORGOT_PASSWORD.created_at.desc())
            .first()
        )
        if not reset_entry:
            return {"error": "Invalid token! Please try again later"}, 400

        

        if datetime.utcnow() > reset_entry.expires_at:
            return {"error": "Link expired! Try again."}, 400

        hashed_password = generate_password_hash(new_password)

        user = USER.query.filter_by(id=reset_entry.user_id).first()
        user.password_hash = hashed_password
        db.session.commit()

        return {"message": "Password reset successfully"}, 200
    except OperationalError:
        return {"error": "Database not reachable"}, 503

    except Exception as e:
        db.session.rollback()
        return {"error": "Error resetting password"}, 500


def change_password_service(data, email):
    old_password = data["old_password"]
    new_password = data["new_password"]

    try:
        user = USER.query.filter_by(email=email).first()

        if not user:
            return {"error": "User not found"}, 404

        if not check_password_hash(user.password_hash, old_password):
            return {"error": "Wrong old password"}, 401

        hashed_password = generate_password_hash(new_password)

        user.password_hash = hashed_password
        db.session.commit()

        return {"message": "Password change successfully"}, 200
    except OperationalError:
        return {"error": "Database not reachable"}, 503

    except Exception as e:
        db.session.rollback()
        return {"error": "Error Change password"}, 500
