from datetime import datetime

from app import db
from const import AnnotationStatus


class Annotation(db.Model):
    __tablename__ = "annotations"

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(
        db.Integer, db.ForeignKey("pdf_documents.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String, nullable=False)
    layer = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, default=AnnotationStatus.ACTIVE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    document = db.relationship("PDFDocument", back_populates="annotations")
    user = db.relationship("User")
    comments = db.relationship(
        "Comment", backref="annotation", lazy=True, cascade="all, delete-orphan"
    )

    __mapper_args__ = {"polymorphic_identity": "annotation", "polymorphic_on": status}


class DrawingAnnotation(Annotation):
    __tablename__ = "drawing_annotations"

    id = db.Column(db.Integer, db.ForeignKey("annotations.id"), primary_key=True)
    path = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    width = db.Column(db.Float, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "drawing"}


class HighlightAnnotation(Annotation):
    __tablename__ = "highlight_annotations"

    id = db.Column(db.Integer, db.ForeignKey("annotations.id"), primary_key=True)
    text_range = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "highlight"}
