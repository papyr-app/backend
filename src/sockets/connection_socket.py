def handle_connections(socketio):
    @socketio.on("connect")
    def handle_connect():
        pass

    @socketio.on("disconnect")
    def handle_disconnect():
        pass

    @socketio.on("join_room")
    def on_join(data):
        pass

    @socketio.on("leave_room")
    def on_leave(data):
        pass
