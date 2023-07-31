from datetime import datetime, timedelta

from app import db


class Posts(db.Model):
    """Модель постов."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(124), nullable=False)
    image = db.Column(db.String(128))
    text = db.Column(db.Text, unique=True)
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow() + timedelta(hours=3)
    )
    added_by = db.Column(db.String(64))
