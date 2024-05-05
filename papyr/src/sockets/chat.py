def message_received(methods=['GET', 'POST']):
    print('message was received!!!')


def handle_chat(socketio):
    @socketio.on('my event')
    def handle_my_custom_event(json, methods=['GET', 'POST']):
        print('received my event: ' + str(json))
        socketio.emit('my response', json, callback=message_received)
