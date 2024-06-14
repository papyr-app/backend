def handle_annotations(socketio):
    @socketio.on("create_annotation")
    def handle_create_annotation(data):
        pass

    @socketio.on("update_annotation")
    def handle_update_annotation(data):
        pass

    @socketio.on("delete_annotation")
    def handle_delete_annotation(data):
        pass
