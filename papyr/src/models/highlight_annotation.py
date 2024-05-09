from mongoengine import StringField

from const import AnnotationType
from models.annotation import Annotation


class HighlightAnnotation(Annotation):
    text_range = StringField(required=True)
    color = StringField(required=True)
    annotation_type = StringField(default=AnnotationType.HIGHLIGHT)

    meta = {'collection': 'annotations'}
