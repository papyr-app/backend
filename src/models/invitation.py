from datetime import datetime, timedelta

from app import db


class Invitation(db.Model):
    __tablename__ = "invitations"

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(
        db.Integer, db.ForeignKey("pdf_documents.id"), nullable=False
    )
    invited_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    invitee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    expires_at = db.Column(
        db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=7)
    )

    document = db.relationship("PDFDocument", back_populates="invitations")
    invited_by = db.relationship("User", foreign_keys=[invited_by_id])
    invitee = db.relationship("User", foreign_keys=[invitee_id])

    def has_access(self, user_id):
        return self.invitee.id == user_id or self.invited_by.id == user_id
