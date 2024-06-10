from bson import ObjectId
from typing import List

from errors import AuthorizationError
from models.invitation import Invitation
from models.pdf_document import PDFDocument
from models.user import User


def get_invitation(invitation_id: ObjectId) -> Invitation:
    return Invitation.objects(id=invitation_id).get()


def get_invitation_check_access(invitation_id: int, user_id: ObjectId) -> Invitation:
    """
    Retrieves an invitation and checks if the user has access to it.

    :param invitation_id: The ID of the invitation to retrieve.
    :type invitation_id: int
    :param user_id: The ID of the user requesting access to the invitation.
    :type user_id: ObjectId
    :raises AuthorizationError: If the user does not have access to the invitation.
    :return: The invitation if access is granted.
    :rtype: Invitation
    """
    invitation = Invitation.objects(id=ObjectId(invitation_id)).get()
    if not invitation.has_access(user_id):
        raise AuthorizationError()
    return invitation


def get_sent_invitations(user_id: ObjectId) -> List[Invitation]:
    return Invitation.objects(invited_by=user_id).all()


def get_received_invitations(user_id: ObjectId) -> List[Invitation]:
    return Invitation.objects(invitee=user_id).all()


def create_invitation(
    document: PDFDocument, invited_by: User, invitee: User
) -> Invitation:
    invitation = Invitation(
        document=document,
        invited_by=invited_by,
        invitee=invitee,
    )
    invitation.save()
    return invitation
