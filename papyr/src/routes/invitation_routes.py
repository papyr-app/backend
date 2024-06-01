from datetime import datetime
from flask import request, jsonify, Blueprint
from mongoengine.errors import DoesNotExist
from marshmallow import ValidationError

from errors import AuthorizationError
from auth.decorators import token_required
from models.user import User
from services import user_service
from services import document_service
from services import invitation_service
from schemas.invitation_schema import CreateInvitationSchema, AcceptInvitationSchema


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
        schema = CreateInvitationSchema()
        try:
            validated_data = schema.load(data)
            invitee = user_service.get_user_by_email(validated_data['invitee'])
            document = document_service.get_document_check_access(validated_data['document'], user.id)

            if user != document.owner:
                return jsonify({'error': 'Only the owner can invite users to documents.'}), 400

            if user == invitee:
                return jsonify({'error': 'Cannot invite yourself to a document.'}), 400

            if invitee in document.collaborators:
                return jsonify({'error': 'User is already a collaborator.'}), 400

            invitation = invitation_service.create_invitation(document, user, invitee)
            return jsonify({'data': invitation.to_mongo().to_dict()}), 201
        except ValidationError as err:
            return jsonify({'error': str(err)}), 400
        except Exception as err:
            return jsonify({'error': str(err)}), 500

    @invitation_bp.route('/accept', methods=['POST'])
    @token_required
    def accept_invitation(user: User):
        data = request.get_json()
        schema = AcceptInvitationSchema()
        try:
            validated_data = schema.load(data)
            invitation = invitation_service.get_invitation_check_access(validated_data['invitation'], user.id)

            if invitation.invitee != user:
                return jsonify({'error': 'Invitation is not for you'}), 400

            if invitation.expires_at < datetime.utcnow():
                return jsonify({'error': 'Invitation is expired'}), 400

            user = user_service.get_user_by_id(user.id)
            document_service.add_collaborator(user, invitation.document)
            return jsonify({'data': 'Granted access to document'}), 201
        except ValidationError as err:
            return jsonify({'error': str(err)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return invitation_bp
