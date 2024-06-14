import uuid
from datetime import datetime, timedelta

from app import db, bcrypt
from const import RoleType, DocumentStatus

# Association table for the many-to-many relationship
document_collaborators = db.Table(
    "document_collaborators",
    db.Column(
        "pdf_document_id",
        db.Integer,
        db.ForeignKey("pdf_documents.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)


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

    document = db.relationship("PDFDocument", backref="invitations")
    invited_by = db.relationship(
        "User", foreign_keys=[invited_by_id], backref="invited_invitations"
    )
    invitee = db.relationship(
        "User", foreign_keys=[invitee_id], backref="received_invitations"
    )

    def has_access(self, user_id):
        return self.invitee.id == user_id or self.invited_by.id == user_id


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

    owner = db.relationship("User", backref="owned_documents")
    collaborators = db.relationship(
        "User", secondary=document_collaborators, backref="collaborations"
    )
    virtual_paths = db.relationship(
        "VirtualPath", backref="pdf_document", cascade="all, delete-orphan"
    )

    def has_access(self, user_id: int) -> bool:
        return self.owner.id == user_id or user_id in [
            collaborator.id for collaborator in self.collaborators
        ]


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default=RoleType.USER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def record_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()


class VirtualPath(db.Model):
    __tablename__ = "virtual_paths"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    document_id = db.Column(
        db.Integer,
        db.ForeignKey("pdf_documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    file_path = db.Column(db.String, default="", nullable=False)

    user = db.relationship("User", backref="virtual_paths")
