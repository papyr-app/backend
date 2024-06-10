from marshmallow import Schema, fields, validate

from const import AnnotationStatus


class CreateAnnotationSchema(Schema):
    document = fields.Str(required=True)
    user = fields.Str(required=True)
    page_number = fields.Int(required=True, validate=validate.Range(min=1))
    position = fields.Str(required=True)
    layer = fields.Int(required=True)
    status = fields.Str(
        required=True,
        validate=validate.OneOf(["active", "archived"]),
        default=AnnotationStatus.ACTIVE,
    )


class UpdateAnnotationSchema(Schema):
    id = fields.Str(required=True)
    page_number = fields.Int(required=False, validate=validate.Range(min=1))
    position = fields.Str(required=False)
    layer = fields.Int(required=False)
    status = fields.Str(required=False, validate=validate.OneOf(["active", "archived"]))
