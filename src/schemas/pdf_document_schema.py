from werkzeug.datastructures import ImmutableMultiDict
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import (
    Schema,
    fields,
    validates,
    validate,
    post_dump,
    pre_load,
    ValidationError,
)

from src.app import db
from src.models import PDFDocument, VirtualPath
from src.const import DocumentStatus
from src.schemas.user_schema import UserSchema
from src.utils.helper import clean_path


class PDFDocumentSchema(SQLAlchemyAutoSchema):
    owner = fields.Nested(UserSchema)

    class Meta:
        model = PDFDocument
        include_fk = True
        load_instance = True
        sqla_session = db.session

    @post_dump(pass_many=False)
    def add_file_path(self, data, many, **kwargs):
        user = self.context.get("user")
        if user:
            virtual_path = db.session.query(VirtualPath).filter_by(user_id=user.id, document_id=data["id"]).first()
            if virtual_path:
                data["file_path"] = virtual_path.file_path
        return data


class CreatePDFDocumentSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=40))
    description = fields.String(required=False, validate=validate.Length(max=300))
    can_share = fields.Boolean(required=False, dump_default=False)
    file_path = fields.String(required=True, validate=validate.Length(max=100))

    @pre_load
    def process_input(self, data, **kwargs):
        if isinstance(data, ImmutableMultiDict):
            data = data.to_dict()

        if "file_path" not in data:
            raise ValidationError("file_path is required.")

        data["file_path"] = clean_path(data["file_path"])
        return data


class UpdatePDFDocumentSchema(Schema):
    title = fields.String(required=False, validate=validate.Length(min=1, max=40))
    description = fields.String(required=False, validate=validate.Length(max=300))
    status = fields.String(required=False)
    can_share = fields.Boolean(required=False)
    file_path = fields.String(required=False, validate=validate.Length(max=100))

    @pre_load
    def process_input(self, data, **kwargs):
        if "file_path" in data:
            data["file_path"] = clean_path(data["file_path"])
        return data

    @validates("status")
    def validate_status(self, value):
        if value not in DocumentStatus.__members__:
            raise ValidationError("Invalid status.")
