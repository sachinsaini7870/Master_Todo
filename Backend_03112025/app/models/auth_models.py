from ..extensions import db
from ..utils.time_conversion import utc_to_ist, to_iso
from datetime import datetime
from sqlalchemy import Text


class USER(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, comment="primary key of user")

    username = db.Column(
        db.String(100), unique=True, nullable=False, comment="username of the user"
    )

    email = db.Column(
        db.String(150), unique=True, nullable=False, comment="email id of user"
    )
    email_verified = db.Column(
        db.Boolean, default=False, comment="email verification boolean"
    )

    password_hash = db.Column(
        db.String(255), nullable=False, comment="encrypted password of user"
    )

    status = db.Column(
        db.String(20), default="pending", comment="active, pending, block, delete"
    )

    # created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc))
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, comment="time of user created"
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="time of user update",
    )

    todos = db.relationship(
        "Todo", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    otps = db.relationship(
        "OTP", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "email_verified": self.email_verified,
            "status": self.status,
            "created_at": to_iso(utc_to_ist(self.created_at)),
            "updated_at": to_iso(utc_to_ist(self.updated_at)),
        }

    def __repr__(self):
        """Official string representation of the User object for debugging."""
        return f"<User id={self.id}, username={self.username}, email={self.email}, status={self.status}, created_at={to_iso(utc_to_ist(self.created_at))}, updated_at={to_iso(utc_to_ist(self.updated_at))}>"


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

    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="created time")
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="update time",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "purpose": self.purpose,
            "expires_at": self.expires_at,
            "attempt_count": self.attempt_count,
            "created_at": to_iso(utc_to_ist(self.created_at)),
            "updated_at": to_iso(utc_to_ist(self.updated_at)),
        }

    def __repr__(self):
        """Official string representation of the User object for debugging."""
        return f"<User id={self.id}, purpose={self.purpose}, expire_at={self.expire_at}, attempt_count={self.attempt_count}, created_at={to_iso(utc_to_ist(self.created_at))}, updated_at={to_iso(utc_to_ist(self.updated_at))}>"



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

    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="created time")
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="update time",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "expires_at": self.expires_at,
            "created_at": to_iso(utc_to_ist(self.created_at)),
            "updated_at": to_iso(utc_to_ist(self.updated_at)),
        }

    def __repr__(self):
        """Official string representation of the User object for debugging."""

        data = f"""<Reset id={self.id}, user_id={self.user_id}, expires_at={self.expires_at}, created_at={to_iso(utc_to_ist(self.created_at))}, updated_at={to_iso(utc_to_ist(self.updated_at))}>"""

        return data
