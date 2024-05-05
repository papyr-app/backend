from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect


def handle_chat(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('A user connected.')
        emit('server_response', {'message': 'You are connected!'})

    @socketio.on('disconnect')
    def handle_disconnect():
        print('User disconnected.')

    @socketio.on('join_room')
    def on_join(data):
        username = data['username']
        room = data.get('room', 'default_room')
        join_room(room)
        socketio.emit('server_response', {'message': f'{username} has entered the room.'}, room=room)

    @socketio.on('leave_room')
    def on_leave(data):
        username = data['username']
        room = data.get('room', 'default_room')
        leave_room(room)
        socketio.emit('server_response', {'message': f'{username} has left the room.'}, room=room)

    @socketio.on('send_message')
    def handle_message(data):
        room = data.get('room', 'default_room')
        print(f"Message received: {data['message']} from {data.get('username', 'Anonymous')}")
        emit('new_message', {'username': data.get('username', 'Anonymous'), 'message': data['message']}, room=room)
