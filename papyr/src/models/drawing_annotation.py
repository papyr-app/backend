from mongoengine import StringField

from models.annotation import Annotation


class DrawingAnnotation(Annotation):
    text_range = StringField(required=True)
    color = StringField(required=True)

    meta = {'collection': 'drawing_annotations'}
