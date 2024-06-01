from marshmallow import fields

from schemas.annotation_schema import CreateAnnotationSchema, UpdateAnnotationSchema


class CreateHighlightAnnotationSchema(CreateAnnotationSchema):
    text_range = fields.Str(required=True)
    color = fields.Str(required=True)
    annotation_type = fields.Str(required=True)


class HighlightAnnotationUpdateSchema(UpdateAnnotationSchema):
    text_range = fields.Str(required=True)
    color = fields.Str(required=True)
    annotation_type = fields.Str(required=True)
