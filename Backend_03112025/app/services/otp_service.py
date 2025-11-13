from .auth_service import generate_otp
from ..extensions import db
from ..models.user_model import User  # User model from SQLAlchemy
from ..models.otp_model import OTP
from datetime import datetime, timedelta  # To set token expiration time
from flask_jwt_extended import create_access_token  # To generate JWT access tokens
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from ..utils.send_email import send_otp_email


def resend_register_otp_service(data):
    email = data["email"]
    purpose = data["purpose"]

    try:
        # ✅ Fetch user
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 404

        # ✅ User must still be pending
        if user.status != "pending":
            return {"error": "User already registered"}, 400

        # ✅ Count today's OTP generation
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

        # ✅ Mark previous OTP as used
        last_otp = (
            OTP.query.filter_by(user_id=user.id, purpose=purpose, is_used=False)
            .order_by(OTP.created_at.desc())
            .first()
        )

        if last_otp:
            last_otp.is_used = True
            db.session.commit()

        # ✅ Generate new OTP
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
    purpose = data["purpose"]

    try:
        # Fetch user
        user = User.query.filter_by(email=email).first()
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
        token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(hours=24)
        )

        return {"message": "OTP verified successfully", "token": token}, 200

    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError as err:
        db.session.rollback()
        return {"error": "Database error", "err": err}, 500


def forgot_otp_service(data):
    email = data["email"]
    purpose = data["purpose"] or "forgot"

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 404

        if user.status != "active":
            return {"error": "Inactive user"}, 400

        # count today OTPs
        today_start = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        count_today = OTP.query.filter(
            OTP.user_id == user.id,
            OTP.purpose == purpose,
            OTP.created_at >= today_start,
        ).count()

        if count_today >= 5:
            return {"error": "Max OTP limit reached for today"}, 429

        # Mark previous unused as used
        last_otp = (
            OTP.query.filter_by(user_id=user.id, purpose=purpose, is_used=False)
            .order_by(OTP.created_at.desc())
            .first()
        )

        if last_otp:
            last_otp.is_used = True
            db.session.commit()

        # Generate new OTP
        new_otp = generate_otp()

        otp_entry = OTP(
            user_id=user.id,
            otp=new_otp,
            purpose=purpose,
            channel="email",
            expires_at=datetime.utcnow() + timedelta(minutes=5),
        )
        db.session.add(otp_entry)
        db.session.commit()

        send_otp_email(user.email, new_otp)

        return {
            "message": "Forgot OTP sent",
            # "otp": new_otp,  # dev only
            "user_id": user.id,
        }, 200

    except Exception as err:
        db.session.rollback()
        return {"error": str(err)}, 500


def verify_forgot_otp_service(data):
    email = data.get("email")
    entered_otp = data["otp"]
    purpose = data["purpose"]

    try:
        # Fetch user
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 404

        # User must be pending
        if (user.status == "pending") or (user.status == "delete"):
            return {"error": "User not regitered, active or invalid status"}, 400

        # Fetch latest OTP
        otp_obj = (
            OTP.query.filter_by(
                user_id=user.id, purpose=purpose or "forgot", is_used=False
            )
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
            identity=str(user.id), fresh=True, additional_claims=additional_claims
        )

        return {"message": "OTP verified successfully", "token": token}, 200

    except OperationalError:
        return {"error": "Database not reachable"}, 503
    except SQLAlchemyError as err:
        db.session.rollback()
        return {"error": "Database error", "err": err}, 500
