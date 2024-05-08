import uuid

from models.invitation import Invitation
from models.pdf_document import PDFDocument
from models.user import User


def get_invitation(invite_id: str) -> Invitation:
    return Invitation.objects(invite_id=invite_id).get()


def create_invitation(invitee: User, document: PDFDocument):
    invitation = Invitation(
            invite_id=generate_unique_invite_id(),
            document=PDFDocument,
            invited_by=User,
    )
    invitation.save()
    return invitation


def generate_unique_invite_id():
    return str(uuid.uuid4())
