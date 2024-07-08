from flask import Blueprint


def create_health_bp():
    health_bp = Blueprint("health", __name__, url_prefix="/api/health")

    @health_bp.route("", methods=["GET"])
    def health_check():
        return "OK", 200

    return health_bp
