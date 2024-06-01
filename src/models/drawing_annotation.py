from mongoengine import StringField, FloatField

from const import AnnotationType
from models.annotation import Annotation


class DrawingAnnotation(Annotation):
    path = StringField(required=True)
    color = StringField(required=True)
    width = FloatField(required=True)
    annotation_type = StringField(AnnotationType.DRAWING)
