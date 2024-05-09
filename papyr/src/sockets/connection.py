import logging
from flask_socketio import emit, join_room, leave_room


def handle_connections(socketio):
    @socketio.on('connect')
    def handle_connect():
        logging.info('A user connected.')
        emit('server_response', {'message': 'You are connected!'})

    @socketio.on('disconnect')
    def handle_disconnect():
        logging.info('User disconnected.')

    @socketio.on('join_room')
    def on_join(data):
        logging.info(data)
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
