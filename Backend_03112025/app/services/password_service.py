from ..extensions import db
from ..models.user_model import USER
from werkzeug.security import generate_password_hash


def reset_password_service(data):
    email = data["email"]
    new_password = data["new_password"]

    try:
        user = USER.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found"}, 404

        # set new password
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        return {
            "message": "Password reset successfully"
        }, 200

    except Exception as err:
        db.session.rollback()
        return {"error": str(err)}, 500


