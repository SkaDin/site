from datetime import datetime, timedelta

from app import db


class Post(db.Model):
    """Модель постов."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(17), nullable=False)
    image = db.Column(db.String(128))
    text = db.Column(db.Text, unique=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow() + timedelta(hours=3)
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="posts")
