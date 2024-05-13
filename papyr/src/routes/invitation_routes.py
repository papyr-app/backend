from datetime import datetime
from flask import request, jsonify, Blueprint
from mongoengine.errors import DoesNotExist

from models.pdf_document import PDFDocument
from models.user import User
from models.invitation import Invitation
from services import user_service
from services import document_service
from services import invitation_service


def create_invitation_bp():
    invitation_bp = Blueprint('invitation', __name__, url_prefix='/api/invitation')

    @invitation_bp.route('/<invitation_id>', methods=['GET'])
    def get_invitation(invitation_id: int):
        try:
            invitation = invitation_service.get_invitation(invitation_id)
            return jsonify(invitation.to_mongo().to_dict()), 201
        except DoesNotExist:
            return jsonify({'error': 'Invitation does not exist'}), 400

    @invitation_bp.route('/<user_id>/sent', methods=['GET'])
    def get_sent_invitations(user_id: int):
        invitations = invitation_service.get_sent_invitations(user_id)
        return jsonify([inv.to_mongo().to_dict() for inv in invitations]), 201

    @invitation_bp.route('/<user_id>/received', methods=['GET'])
    def get_received_invitations(user_id: int):
        invitations = invitation_service.get_received_invitations(user_id)
        return jsonify([inv.to_mongo().to_dict() for inv in invitations]), 201

    @invitation_bp.route('/invite', methods=['POST'])
    def create_invitation():
        data = request.get_json()
        # TODO - get user id from JWT
        user_id = data.get('user_id')
        email = data.get('email')
        document_id = data.get('document_id')

        # TODO - check if user has permissions to invite

        if not email or not document_id or not user_id:
            return jsonify({'error': 'Missing required fields'})

        try:
            document = document_service.get_document(document_id)
            invited_by = user_service.get_user_by_id(user_id)
            invitee = user_service.get_user_by_email(email)
            invitation = invitation_service.create_invitation(document, invited_by, invitee)
            return jsonify(invitation.to_mongo().to_dict()), 200
        except PDFDocument.DoesNotExist:
            return jsonify({'error': 'Document does not exist'}), 400
        except User.DoesNotExist:
            return jsonify({'error': 'User does not exist'}), 400

    @invitation_bp.route('/accept', methods=['POST'])
    def accept_invitation():
        data = request.get_json()
        # TODO - get user id from JWT
        user_id = data.get('user_id')
        invitation_id = data.get('invitation_id')

        # TODO - check if user has permissions to invite

        if not user_id or not invitation_id:
            return jsonify({'error': 'Missing required fields'})

        try:
            invitation = invitation_service.get_invitation(invitation_id)

            if invitation.expires_at < datetime.utcnow():
                return jsonify({'error': 'Invitation is expired'}), 400

            user = user_service.get_user_by_id(user_id)
            document_service.add_collaborator(user, invitation.document)

            return "You have been granted access to the document.", 200
        except PDFDocument.DoesNotExist:
            return jsonify({'error': 'Document does not exist'}), 400
        except Invitation.DoesNotExist:
            return jsonify({'error': 'Invitation does not exist'}), 400
        except User.DoesNotExist:
            return jsonify({'error': 'User does not exist'}), 400

    return invitation_bp
