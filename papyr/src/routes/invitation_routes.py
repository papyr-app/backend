from datetime import datetime
from flask import request, jsonify, Blueprint
from mongoengine.errors import DoesNotExist

from errors import AuthorizationError
from auth.decorators import token_required
from models.pdf_document import PDFDocument
from models.user import User
from models.invitation import Invitation
from services import user_service
from services import document_service
from services import invitation_service


def create_invitation_bp():
    invitation_bp = Blueprint('invitation', __name__, url_prefix='/api/invitation')

    @invitation_bp.route('/<invitation_id>', methods=['GET'])
    @token_required
    def get_invitation(user: User, invitation_id: int):
        try:
            invitation = invitation_service.get_invitation_check_access(invitation_id, user.id)
            return jsonify({'data': invitation.to_mongo().to_dict()}), 200
        except DoesNotExist:
            return jsonify({'error': 'Invitation does not exist'}), 400
        except AuthorizationError as e:
            return jsonify({'error': str(e)}), 403
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @invitation_bp.route('/sent', methods=['GET'])
    @token_required
    def get_sent_invitations(user: User):
        try:
            invitations = invitation_service.get_sent_invitations(user.id)
            return jsonify({'data': [inv.to_mongo().to_dict() for inv in invitations]}), 200
        except AuthorizationError as e:
            return jsonify({'error': str(e)}), 403
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @invitation_bp.route('/received', methods=['GET'])
    @token_required
    def get_received_invitations(user: User):
        try:
            invitations = invitation_service.get_received_invitations(user.id)
            return jsonify({'data': [inv.to_mongo().to_dict() for inv in invitations]}), 200
        except AuthorizationError as e:
            return jsonify({'error': str(e)}), 403
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @invitation_bp.route('/invite', methods=['POST'])
    @token_required
    def create_invitation(user: User):
        data = request.get_json()
        email = data.get('email')
        document_id = data.get('document_id')

        if not email or not document_id:
            return jsonify({'error': 'Missing required fields'})

        try:
            invited_by = user_service.get_user_by_id(user.id)
            invitee = user_service.get_user_by_email(email)
            document = document_service.get_document_check_access(document_id, user.id)
            invitation = invitation_service.create_invitation(document, invited_by, invitee)
            return jsonify({'data': invitation.to_mongo().to_dict()}), 201
        except PDFDocument.DoesNotExist:
            return jsonify({'error': 'Document does not exist'}), 400
        except User.DoesNotExist:
            return jsonify({'error': 'User does not exist'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @invitation_bp.route('/accept', methods=['POST'])
    @token_required
    def accept_invitation(user: User):
        data = request.get_json()
        invitation_id = data.get('invitation_id')

        if not invitation_id:
            return jsonify({'error': 'Missing required fields'})

        try:
            invitation = invitation_service.get_invitation_check_access(invitation_id, user.id)

            if invitation.expires_at < datetime.utcnow():
                return jsonify({'error': 'Invitation is expired'}), 400

            user = user_service.get_user_by_id(user.id)
            document_service.add_collaborator(user, invitation.document)
            return jsonify({'data': 'Granted access to document'}), 201
        except PDFDocument.DoesNotExist:
            return jsonify({'error': 'Document does not exist'}), 400
        except Invitation.DoesNotExist:
            return jsonify({'error': 'Invitation does not exist'}), 400
        except User.DoesNotExist:
            return jsonify({'error': 'User does not exist'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return invitation_bp
