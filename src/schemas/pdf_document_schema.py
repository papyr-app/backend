from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, validate, pre_load, ValidationError

from models.pdf_document import PDFDocument
from const import DocumentStatus
from utils.helper import clean_path


class PDFDocumentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PDFDocument
        include_fk = True
        load_instance = True


class CreatePDFDocumentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PDFDocument
        load_instance = True
        include_fk = True

    title = fields.String(required=True, validate=validate.Length(min=1, max=40))
    description = fields.String(required=False, validate=validate.Length(max=300))
    can_share = fields.Boolean(required=False, default=False)
    file_path = fields.String(required=True, validate=validate.Length(max=100))

    @pre_load
    def process_input(self, data, **kwargs):
        data["file_path"] = clean_path(data["file_path"])
        return data


class UpdatePDFDocumentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PDFDocument
        load_instance = True
        include_fk = True

    title = fields.String(required=False, validate=validate.Length(min=1, max=40))
    description = fields.String(required=False, validate=validate.Length(max=300))
    status = fields.String(required=False)
    can_share = fields.Boolean(required=False)
    file_path = fields.String(required=False, validate=validate.Length(max=100))

    @pre_load
    def process_input(self, data, **kwargs):
        data["file_path"] = clean_path(data["file_path"])
        return data

    @validates("status")
    def validate_status(self, value):
        if value not in DocumentStatus.__members__:
            raise ValidationError("Invalid status.")
