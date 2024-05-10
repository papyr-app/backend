from marshmallow import fields

from schemas.annotation_schema import AnnotationSchema, AnnotationUpdateSchema


class HighlightAnnotationSchema(AnnotationSchema):
    text_range = fields.Str(required=True)
    color = fields.Str(required=True)
    annotation_type = fields.Str(required=True)


class HighlightAnnotationUpdateSchema(AnnotationUpdateSchema):
    text_range = fields.Str(required=True)
    color = fields.Str(required=True)
    annotation_type = fields.Str(required=True)
