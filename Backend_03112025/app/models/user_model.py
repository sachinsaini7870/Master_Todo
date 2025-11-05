from datetime import datetime, timezone
from ..extensions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_ad = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc))

    todos = db.relationship(
        "Todo", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}
    
    def __repr__(self):
        """Official string representation of the User object for debugging."""
        return f"<User id={self.id} username={self.username} email={self.email}>"
