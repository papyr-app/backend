from mongoengine import StringField

from models.annotation import Annotation


class HighlightAnnotation(Annotation):
    text_range = StringField(required=True)
    color = StringField(required=True)

    meta = {'collection': 'highlight_annotations'}
