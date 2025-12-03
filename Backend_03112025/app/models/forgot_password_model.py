# Backend_03112025\app\models\otp_model.py
from ..extensions import db
from sqlalchemy import Text
from ..utils.time_conversion import to_indianStandardTime


class FORGOT_PASSWORD(db.Model):
    __tablename__ = "forgot_password"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_forgot_user", ondelete="CASCADE"),
        nullable=False,
        comment="link with users table id",
    )

    token = db.Column(
        Text,
        nullable=False,
        comment="store jwt token after verify of email and mobile",
    )  # always as string

    expires_at = db.Column(db.DateTime, nullable=False, comment="time for expire otp")

    created_at = db.Column(db.DateTime, default=db.func.now(), comment="created time")
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now(),
        comment="update time",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "expires_at": self.expires_at,
            "created_at": str(to_indianStandardTime(self.created_at)),
            "updated_at": str(to_indianStandardTime(self.updated_at)),
        }

    def __repr__(self):
        """Official string representation of the User object for debugging."""
        
        data = f"""<Reset id={self.id}, user_id={self.user_id}, expires_at={self.expires_at}, created_at={str(to_indianStandardTime(self.created_at))}, updated_at={str(to_indianStandardTime(self.updated_at))}>"""
        
        return data
