from marshmallow import Schema, fields, validate, validates, pre_load, ValidationError

from models.pdf_document import PDFDocument
from utils.helper import clean_path


class CreateVirtualPathSchema(Schema):
    document = fields.String(required=True)
    file_path = fields.String(required=True, validate=validate.Length(max=100))

    @validates("document")
    def validate_document(self, value):
        if not PDFDocument.objects(id=value).first():
            raise ValidationError("Document not found.")

    @pre_load
    def process_input(self, data, **kwargs):
        data["file_path"] = clean_path(data["file_path"])
        return data


class UpdateVirtualPathSchema(Schema):
    file_path = fields.String(required=True, validate=validate.Length(max=100))

    @pre_load
    def process_input(self, data, **kwargs):
        data["file_path"] = clean_path(data["file_path"])
        return data
