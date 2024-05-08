import logging
from flask_socketio import emit, join_room, leave_room

from models.comment import Comment


def handle_comments(socketio):
    @socketio.on('create_comment')
    def handle_create_comment(data):
        # TODO - Extract information from data (assuming data includes annotation_id, user_id, and content)
        # TODO - Create a new comment in the database
        # TODO - Notify all clients that are subscribed to updates for this annotation
        pass

    @socketio.on('update_comment')
    def handle_update_comment(data):
        # TODO - Check user permissions to ensure they can update the comment
        # TODO - Find the comment by ID, update its content, and save the changes
        # TODO - Broadcast the updated comment to all clients viewing the same annotation
        pass

    @socketio.on('delete_comment')
    def handle_delete_comment(data):
        # TODO - Verify user permission to delete the comment
        # TODO - Locate the comment by ID and delete it from the database
        # TODO - Inform all clients viewing the annotation of the comment deletion
        pass
