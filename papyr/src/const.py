from enum import StrEnum


class DocumentStatus(StrEnum):
    PENDING = 'pending'
    ONGOING = 'ongoing'
    COMPLETE = 'complete'


class AnnotationType(StrEnum):
    HIGHLIGHT = 'highlight'
    DRAWING = 'drawing'
