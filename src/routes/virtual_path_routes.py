import logging
from flask import request, jsonify, Blueprint
from mongoengine.errors import DoesNotExist
from marshmallow import ValidationError

from auth.decorators import token_required
from services import virtual_path_service
from models.user import User
from schemas.virtual_path_schema import CreateVirtualPathSchema, UpdateVirtualPathSchema


def create_virtual_path_bp():
    virtual_path_bp = Blueprint(
        "virtual_path", __name__, url_prefix="/api/virtual_path"
    )

    @virtual_path_bp.route("", methods=["POST"])
    @token_required
    def create_virtual_path(user: User):
        data = request.json
        create_schema = CreateVirtualPathSchema()
        try:
            validated_data = create_schema.load(data)
            virtual_path = virtual_path_service.create_virtual_path(
                user, **validated_data
            )
            return jsonify({"data": virtual_path.to_mongo().to_dict()}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            logging.error(err)
            return jsonify({"error": str(err)}), 500

    @virtual_path_bp.route("/<virtual_path_id>", methods=["PATCH"])
    @token_required
    def update_virtual_path(user: User, virtual_path_id: str):
        data = request.json
        update_schema = UpdateVirtualPathSchema()
        try:
            validated_data = update_schema.load(data)
            virtual_path = virtual_path_service.get_virtual_path(virtual_path_id)
            virtual_path = virtual_path_service.update_virtual_path(
                virtual_path, validated_data
            )
            return jsonify({"data": virtual_path.to_mongo().to_dict()}), 200
        except ValidationError as err:
            return jsonify({"error": str(err)}), 400
        except DoesNotExist:
            return jsonify({"error": "Virtual path does not exist"}), 404
        except Exception as err:
            logging.error(err)
            return jsonify({"error": str(err)}), 500

    return virtual_path_bp
