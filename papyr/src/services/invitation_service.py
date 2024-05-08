import uuid
from models.invitation import Invitation


def get_invitation(invite_id: str) -> Invitation:
    return Invitation.objects(invite_id=invite_id).get()


def create_invitation():
    pass


def generate_unique_invite_id():
    return str(uuid.uuid4())
