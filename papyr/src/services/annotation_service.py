from models.highlight_annotation import HighlightAnnotation
from models.drawing_annotation import DrawingAnnotation


def create_highlight_annotation(document, user, page_number, position, layer, text_range, color):
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


def update_highlight_annotation(data):
    pass


def delete_highlight_annotation(data):
    pass


def create_drawing_annotation(document, user, page_number, position, layer, text_range, color):
    annotation = DrawingAnnotation(
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


def update_drawing_annotation(data):
    pass


def delete_drawing_annotation(data):
    pass
