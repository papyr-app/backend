from mongoengine import Document, ReferenceField, DateTimeField
from datetime import datetime

from models.user import User
from models.annotation import Annotation


class SeenStatus(Document):
    user = ReferenceField(User, required=True)
    annotation = ReferenceField(Annotation, required=True)
    seen_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "seen_statuses", "ordering": ["-seen_at"]}
