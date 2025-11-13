# Backend_03112025\app\models\otp_model.py
from ..extensions import db
from ..utils.time_conversion import to_indianStandardTime

class OTP(db.Model):
    __tablename__ = "otp"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="link with users table id",
    )

    otp = db.Column(
        db.String(6), nullable=False, comment="store otp of email and mobile"
    )  # always as string

    purpose = db.Column(
        db.String(20), nullable=False, comment="register, forgot, login"
    )  # register/forgot/login
    channel = db.Column(
        db.String(10), nullable=False, comment="email, sms, both"
    )  # email/sms/both

    expires_at = db.Column(db.DateTime, nullable=False, comment="time for expire otp")
    is_used = db.Column(
        db.Boolean, default=False, comment="check otp is used or not boolean"
    )
    attempt_count = db.Column(db.Integer, default=0, comment="how many attempt do")

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
            "purpose": self.purpose,
            "expires_at": self.expires_at,
            "attempt_count": self.attempt_count,
            "created_at": str(to_indianStandardTime(self.created_at)),
            "updated_at": str(to_indianStandardTime(self.updated_at)),
        }

    def __repr__(self):
        """Official string representation of the User object for debugging."""
        return f"<User id={self.id}, purpose={self.purpose}, expire_at={self.expire_at}, attempt_count={self.attempt_count}, created_at={str(to_indianStandardTime(self.created_at))}, updated_at={str(to_indianStandardTime(self.updated_at))}>"