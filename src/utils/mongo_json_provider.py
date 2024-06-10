from flask.json.provider import DefaultJSONProvider
from bson import ObjectId


class MongoJSONProvider(DefaultJSONProvider):
    """
    A wrapper for the default Flask JSON provider.
    """

    def __init__(self, app):
        super().__init__(app)

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)
