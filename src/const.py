from enum import StrEnum


class DocumentStatus(StrEnum):
    ACTIVE = 'active'
    ARCHIVED = 'archived'


class AnnotationStatus(StrEnum):
    ACTIVE = 'active'
    ARCHIVED = 'archived'


class AnnotationType(StrEnum):
    HIGHLIGHT = 'highlight'
    DRAWING = 'drawing'


class RoleType(StrEnum):
    ADMIN = 'admin'
    USER = 'user'
