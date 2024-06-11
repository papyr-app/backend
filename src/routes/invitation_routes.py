from flask import request, jsonify, Blueprint
from marshmallow import ValidationError

from errors import AuthorizationError
from auth.decorators import token_required
from models import User
from services.invitation_service import InvitationService


def create_invitation_bp():
    invitation_bp = Blueprint("invitation", __name__, url_prefix="/api/invitation")

    @invitation_bp.route("/<invitation_id>", methods=["GET"])
    @token_required
    def get_invitation(user: User, invitation_id: int):
        try:
            invitation = InvitationService.get_invitation_by_id(invitation_id, user.id)
            return jsonify({"data": invitation}), 200
        except AuthorizationError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @invitation_bp.route("/sent", methods=["GET"])
    @token_required
    def get_sent_invitations(user: User):
        try:
            invitations = InvitationService.get_invitations_sent_by_user(user.id)
            return jsonify({"data": invitations}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @invitation_bp.route("/received", methods=["GET"])
    @token_required
    def get_received_invitations(user: User):
        try:
            invitations = InvitationService.get_invitations_received_by_user(user.id)
            return jsonify({"data": invitations}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @invitation_bp.route("/invite", methods=["POST"])
    @token_required
    def create_invitation(user: User):
        data = request.get_json()
        try:
            invitation = InvitationService.create_invitation(data, user)
            return jsonify({"data": invitation}), 201
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            return jsonify({"error": str(err)}), 500

    @invitation_bp.route("/accept", methods=["POST"])
    @token_required
    def accept_invitation(user: User):
        data = request.get_json()
        try:
            invitation = InvitationService.accept_invitation(data, user)
            return jsonify({"data": invitation}), 200
        except AuthorizationError as err:
            return jsonify({"error": str(err)}), 403
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            return jsonify({"error": str(err)}), 500

    return invitation_bp
