import logging
from flask_socketio import emit


def handle_chat(socketio):
    @socketio.on("send_message")
    def handle_message(data):
        room = data.get("room", "default_room")
        logging.info(
            f"Message received: {data['message']} from {data.get('username', 'Anonymous')}"
        )
        emit(
            "new_message",
            {"username": data.get("username", "Anonymous"), "message": data["message"]},
            room=room,
        )
