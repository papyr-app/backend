from marshmallow import Schema, fields, validates, pre_load, ValidationError
from marshmallow_mongoengine import ModelSchema

from models.pdf_document import PDFDocument
from models.virtual_path import VirtualPath
from utils.helper import clean_path


class CreateVirtualPathSchema(ModelSchema):
    class Meta:
        model = VirtualPath

    document = fields.String(required=True)
    file_path = fields.String(required=True)

    @validates('document')
    def validate_document(self, value):
        if not PDFDocument.objects(id=value).first():
            raise ValidationError('Document not found.')

    @pre_load
    def process_input(self, data, **kwargs):
        data['file_path'] = clean_path(data['file_path'])
        return data


class UpdateVirtualPathSchema(Schema):
    file_path = fields.String(required=True)

    @pre_load
    def process_input(self, data, **kwargs):
        data['file_path'] = clean_path(data['file_path'])
        return data
