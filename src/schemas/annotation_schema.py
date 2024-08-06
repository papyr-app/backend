import re
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields, validate, validates, ValidationError

from src.app import db
from src.models import HighlightAnnotation, PDFDocument


class AnnotationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HighlightAnnotation
        load_instance = True
        include_fk = True
        sqla_session = db.session


class CreateAnnotationSchema(Schema):
    document_id = fields.String(required=True)
    page_number = fields.Integer(required=True, validate=validate.Range(min=1))
    quad_points = fields.List(fields.Float(), required=True)
    color = fields.String(required=True)
    opacity = fields.Float(required=True, validate=validate.Range(min=0, max=1))

    @validates("document_id")
    def validate_document(self, value):
        if not db.session.get(PDFDocument, value):
            raise ValidationError("Document not found.")

    @validates("color")
    def validate_color(self, value):
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
            raise ValidationError("Invalid color string")


class UpdateAnnotationSchema(Schema):
    quad_points = fields.List(fields.Float(), required=True)
    color = fields.String(required=True)
    opacity = fields.Float(required=True, validate=validate.Range(min=0, max=1))

    @validates("color")
    def validate_color(self, value):
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
            raise ValidationError("Invalid color string")
