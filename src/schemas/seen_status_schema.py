from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import SeenStatus


class SeenStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SeenStatus
        include_fk = True
        load_instance = True
