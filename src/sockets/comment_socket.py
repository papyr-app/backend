def handle_comments(socketio):
    @socketio.on("create_comment")
    def handle_create_comment(data):
        pass

    @socketio.on("update_comment")
    def handle_update_comment(data):
        pass

    @socketio.on("delete_comment")
    def handle_delete_comment(data):
        pass
