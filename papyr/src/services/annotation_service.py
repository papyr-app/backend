from bson import ObjectId

from models.annotation import Annotation
from models.highlight_annotation import HighlightAnnotation
from models.drawing_annotation import DrawingAnnotation


def get_annotation(annotation_id: int) -> Annotation:
    return Annotation.objects(id=ObjectId(annotation_id)).get()


def create_highlight_annotation(document, user, page_number, position, layer, text_range, color) -> HighlightAnnotation:
    annotation = HighlightAnnotation(
            document=document,
            user=user,
            page_number=page_number,
            position=position,
            layer=layer,
            text_range=text_range,
            color=color
    )
    annotation.save()
    return annotation


def create_drawing_annotation(document, user, page_number, position, layer, path, color, width) -> DrawingAnnotation:
    annotation = DrawingAnnotation(
            document=document,
            user=user,
            page_number=page_number,
            position=position,
            layer=layer,
            path=path,
            color=color,
            width=width
    )
    annotation.save()
    return annotation


def update_annotation(data) -> Annotation:
    pass


def delete_annotation(annotation_id: int):
    annotation = get_annotation(annotation_id)
    annotation.delete()
