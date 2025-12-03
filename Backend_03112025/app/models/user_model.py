# Backend_03112025\app\models\user_model.py
from ..extensions import db
from ..utils.time_conversion import to_indianStandardTime


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
        db.DateTime, default=db.func.now(), comment="time of user created"
    )
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now(),
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
            "created_at": str(to_indianStandardTime(self.created_at)),
            "updated_at": str(to_indianStandardTime(self.updated_at)),
        }

    def __repr__(self):
        """Official string representation of the User object for debugging."""
        return f"<User id={self.id}, username={self.username}, email={self.email}, status={self.status}, created_at={str(to_indianStandardTime(self.created_at))}, updated_at={str(to_indianStandardTime(self.updated_at))}>"
