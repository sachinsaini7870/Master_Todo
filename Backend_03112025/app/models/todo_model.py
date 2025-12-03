# Backend_03112025\app\models\todo_model.py
from ..extensions import db
from ..utils.time_conversion import to_indianStandardTime

class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True, comment="primary key of todo")
    title = db.Column(db.String(150), nullable=False, comment="Title of todo, not null")
    description = db.Column(db.Text, nullable=True, comment="Description of todo")
    completed = db.Column(
        db.Boolean, default=False, nullable=False, comment="complete or pending status"
    )
    status = db.Column(
        db.Boolean, default=True, nullable=False, comment="status for softdelete"
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id", name="fk_todo_user", ondelete="CASCADE", onupdate="RESTRICT"
        ),
        nullable=False,
        comment="This is refrence of primary key of user table",
    )
    created_at = db.Column(
        db.DateTime, default=db.func.now(), comment="time of todo created"
    )
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now(),
        comment="time of todo update",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "user_id": self.user_id,
            "created_at": str(to_indianStandardTime(self.created_at)),
            "updated_at": str(to_indianStandardTime(self.updated_at))
        }

    def __repr__(self):
        """Official string representation of the Todo object for debugging."""
        return f"<Todo id={self.id}, title={self.title}, completed={self.completed}, user_id={self.user_id}, status={self.status}, created_at={str(to_indianStandardTime(self.created_at))}, updated_at={str(to_indianStandardTime(self.updated_at))}>"
