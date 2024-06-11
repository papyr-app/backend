import uuid
from datetime import datetime

from app import db
from const import DocumentStatus


class PDFDocument(db.Model):
    __tablename__ = "pdf_documents"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    status = db.Column(db.String, default=DocumentStatus.ACTIVE)
    can_share = db.Column(db.Boolean, default=False)
    share_token = db.Column(db.String, default=lambda: str(uuid.uuid4()), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    owner = db.relationship("User", foreign_keys=[owner_id])
    collaborators = db.relationship(
        "User", secondary="document_collaborators", back_populates="collaborations"
    )

    def has_access(self, user_id):
        return self.owner.id == user_id or user_id in [
            collaborator.id for collaborator in self.collaborators
        ]
