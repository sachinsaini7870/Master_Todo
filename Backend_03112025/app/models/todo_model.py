from ..extensions import db


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id", name="fk_todo_user", ondelete="CASCADE", onupdate="RESTRICT"
        ),
        nullable=False,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "user_id": self.user_id,
        }

    def __repr__(self):
        """Official string representation of the Todo object for debugging."""
        return f"<Todo id={self.id}, title={self.title}, completed={self.completed}, user_id={self.user_id}, status={self.status}>"