from marshmallow import Schema, fields, validate, validates, pre_load, ValidationError
from marshmallow_mongoengine import ModelSchema
from flask import request

from models.pdf_document import PDFDocument
from const import DocumentStatus


class CreatePDFDocumentSchema(ModelSchema):
    class Meta:
        model = PDFDocument

    title = fields.String(required=True, validate=validate.Length(min=1, max=40))
    description = fields.String(required=False, validate=validate.Length(max=300))
    can_share = fields.Boolean(required=False, default=False)

    @validates('file')
    def validate_file(self, file):
        if not file:
            raise ValidationError('Missing file')
        if not file.filename.endswith('.pdf'):
            raise ValidationError('Only PDF files are allowed')

    @pre_load
    def validate_file_in_request(self, data, **kwargs):
        file = request.files.get('file')
        self.validate_file(file)
        return data


class UpdatePDFDocumentSchema(Schema):
    title = fields.String(required=False, validate=validate.Length(min=1, max=40))
    description = fields.String(required=False, validate=validate.Length(max=300))
    status = fields.String(required=False)
    can_share = fields.Boolean(required=False)

    @validates('status')
    def validate_status(self, value):
        if value not in DocumentStatus.__members__:
            raise ValidationError('Invalid status.')
