from bson import ObjectId
from typing import List

from errors import AuthorizationError
from models.invitation import Invitation
from models.pdf_document import PDFDocument
from models.user import User


def get_invitation(invitation_id: ObjectId) -> Invitation:
    return Invitation.objects(id=invitation_id).get()


def get_invitation_check_access(invitation_id: int, user_id: ObjectId) -> Invitation:
    invitation = Invitation.objects(id=ObjectId(invitation_id)).get()
    if not invitation.has_access(user_id):
        raise AuthorizationError('You are not authorized to access this resource')
    return invitation


def get_sent_invitations(user_id: ObjectId) -> List[Invitation]:
    return Invitation.objects(invited_by=user_id).all()


def get_received_invitations(user_id: ObjectId) -> List[Invitation]:
    return Invitation.objects(invitee=user_id).all()


def create_invitation(document: PDFDocument, invited_by: User, invitee: User):
    invitation = Invitation(
            document=document,
            invited_by=invited_by,
            invitee=invitee,
    )
    invitation.save()
    return invitation
