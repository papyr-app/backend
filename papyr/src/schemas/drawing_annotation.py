from marshmallow import fields

from schemas.annotation_schema import CreateAnnotationSchema, UpdateAnnotationSchema


class CreateDrawingAnnotationSchema(CreateAnnotationSchema):
    path = fields.Str(required=True)
    color = fields.Str(required=True)
    width = fields.Float(required=True)
    annotation_type = fields.Str(required=True)


class HighlightAnnotationUpdateSchema(UpdateAnnotationSchema):
    path = fields.Str(required=True)
    color = fields.Str(required=True)
    width = fields.Float(required=True)
    annotation_type = fields.Str(required=True)
