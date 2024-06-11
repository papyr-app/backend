from datetime import datetime

from app import db


class SeenStatus(db.Model):
    __tablename__ = "seen_statuses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    annotation_id = db.Column(
        db.Integer, db.ForeignKey("annotations.id"), nullable=False
    )
    seen_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")
    annotation = db.relationship("Annotation")
