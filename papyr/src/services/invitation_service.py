from bson import ObjectId
from typing import List

from models.invitation import Invitation
from models.pdf_document import PDFDocument
from models.user import User


def get_invitation(invite_id: int) -> Invitation:
    return Invitation.objects(id=ObjectId(invite_id)).get()


def get_sent_invitations(user_id: int) -> List[Invitation]:
    return Invitation.objects(invited_by=ObjectId(user_id)).all()


def get_received_invitations(user_id: int) -> List[Invitation]:
    return Invitation.objects(invitee=ObjectId(user_id)).all()


def create_invitation(document: PDFDocument, invited_by: User, invitee: User):
    invitation = Invitation(
            document=document,
            invited_by=invited_by,
            invitee=invitee,
    )
    invitation.save()
    return invitation
