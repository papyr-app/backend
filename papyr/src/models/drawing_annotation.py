from mongoengine import StringField, FloatField

from models.annotation import Annotation


class DrawingAnnotation(Annotation):
    path = StringField(required=True)
    color = StringField(required=True)
    width = FloatField(required=True)

    meta = {'collection': 'drawing_annotations'}
