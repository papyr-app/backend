from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate

from src.app import db
from src.models import Annotation, DrawingAnnotation, HighlightAnnotation


class CreateAnnotationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Annotation
        load_instance = True
        include_fk = True
        sqla_session = db.session

    document_id = fields.Str(required=True)
    user_id = fields.Str(required=True)
    page_number = fields.Int(required=True, validate=validate.Range(min=1))
    position = fields.Str(required=True)
    layer = fields.Int(required=True)
    status = fields.Str(
        required=True,
        validate=validate.OneOf(["active", "archived"]),
        default="active",
    )


class UpdateAnnotationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Annotation
        load_instance = True
        include_fk = True
        sqla_session = db.session

    id = fields.Str(required=True)
    page_number = fields.Int(required=False, validate=validate.Range(min=1))
    position = fields.Str(required=False)
    layer = fields.Int(required=False)
    status = fields.Str(required=False, validate=validate.OneOf(["active", "archived"]))


class CreateDrawingAnnotationSchema(CreateAnnotationSchema, SQLAlchemyAutoSchema):
    class Meta:
        model = DrawingAnnotation
        load_instance = True
        include_fk = True
        sqla_session = db.session

    path = fields.Str(required=True)
    color = fields.Str(required=True)
    width = fields.Float(required=True)
    annotation_type = fields.Str(required=True)


class UpdateDrawingAnnotationSchema(UpdateAnnotationSchema, SQLAlchemyAutoSchema):
    class Meta:
        model = DrawingAnnotation
        load_instance = True
        include_fk = True
        sqla_session = db.session

    path = fields.Str(required=False)
    color = fields.Str(required=False)
    width = fields.Float(required=False)
    annotation_type = fields.Str(required=False)


class CreateHighlightAnnotationSchema(CreateAnnotationSchema, SQLAlchemyAutoSchema):
    class Meta:
        model = HighlightAnnotation
        load_instance = True
        include_fk = True
        sqla_session = db.session

    text_range = fields.Str(required=True)
    color = fields.Str(required=True)
    annotation_type = fields.Str(required=True)


class UpdateHighlightAnnotationSchema(UpdateAnnotationSchema, SQLAlchemyAutoSchema):
    class Meta:
        model = HighlightAnnotation
        load_instance = True
        include_fk = True
        sqla_session = db.session

    text_range = fields.Str(required=False)
    color = fields.Str(required=False)
    annotation_type = fields.Str(required=False)
