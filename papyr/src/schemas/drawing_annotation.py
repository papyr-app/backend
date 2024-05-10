from marshmallow import fields

from schemas.annotation_schema import AnnotationSchema, AnnotationUpdateSchema


class DrawingAnnotationSchema(AnnotationSchema):
    path = fields.Str(required=True)
    color = fields.Str(required=True)
    width = fields.Float(required=True)
    annotation_type = fields.Str(required=True)


class HighlightAnnotationUpdateSchema(AnnotationUpdateSchema):
    path = fields.Str(required=True)
    color = fields.Str(required=True)
    width = fields.Float(required=True)
    annotation_type = fields.Str(required=True)
