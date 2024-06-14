import logging
from flask import request, jsonify, Blueprint
from marshmallow import ValidationError

from errors import AuthorizationError
from auth.decorators import token_required
from models import User
from services.invitation_service import InvitationService
from schemas.invitation_schema import InvitationSchema


def create_invitation_bp():
    invitation_bp = Blueprint("invitation", __name__, url_prefix="/api/invitation")

    @invitation_bp.route("/<invitation_id>", methods=["GET"])
    @token_required
    def get_invitation(user: User, invitation_id: int):
        try:
            invitation = InvitationService.get_invitation_by_id(invitation_id)
            InvitationService.check_user_access(invitation, user.id)
            return jsonify({"data": InvitationSchema().dump(invitation)}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except AuthorizationError as err:
            return jsonify({"error": str(err)}), 403
        except Exception as err:
            logging.error(f"Error getting invitation: {str(err)}")
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @invitation_bp.route("/sent", methods=["GET"])
    @token_required
    def get_sent_invitations(user: User):
        try:
            invitations = InvitationService.get_invitations_sent_by_user(user.id)
            return jsonify({"data": InvitationSchema(many=True).dump(invitations)}), 200
        except Exception as err:
            logging.error(f"Error getting sent invitations: {str(err)}")
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @invitation_bp.route("/received", methods=["GET"])
    @token_required
    def get_received_invitations(user: User):
        try:
            invitations = InvitationService.get_invitations_received_by_user(user.id)
            return jsonify({"data": InvitationSchema(many=True).dump(invitations)}), 200
        except Exception as err:
            logging.error(f"Error getting received invitations: {str(err)}")
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @invitation_bp.route("/invite", methods=["POST"])
    @token_required
    def create_invitation(user: User):
        data = request.get_json()
        try:
            invitation = InvitationService.create_invitation(data, user)
            return jsonify({"data": InvitationSchema().dump(invitation)}), 201
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            logging.error(f"Error creating invitation: {str(err)}")
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    @invitation_bp.route("/accept", methods=["POST"])
    @token_required
    def accept_invitation(user: User):
        data = request.get_json()
        try:
            invitation = InvitationService.accept_invitation(data, user)
            return jsonify({"data": InvitationSchema().dump(invitation)}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except AuthorizationError as err:
            return jsonify({"error": str(err)}), 403
        except Exception as err:
            logging.error(f"Error accepting invitation: {str(err)}")
            logging.error("Exception", exc_info=True)
            return jsonify({"error": "Internal error"}), 500

    return invitation_bp
