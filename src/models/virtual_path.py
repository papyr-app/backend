from app import db


class VirtualPath(db.Model):
    __tablename__ = "virtual_paths"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    document_id = db.Column(
        db.Integer,
        db.ForeignKey("pdf_documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    file_path = db.Column(db.String, nullable=False)

    user = db.relationship("User")
    document = db.relationship("PDFDocument", passive_deletes=True)
