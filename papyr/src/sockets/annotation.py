import logging
from flask_socketio import emit, join_room, leave_room

from models.highlight_annotation import HighlightAnnotation
from models.drawing_annotation import DrawingAnnotation


def handle_annotations(socketio):
    @socketio.on('create_annotation')
    def handle_create_annotation(data):
        # TODO - Extract necessary information from data, such as the content of the annotation, the page number, and user_id
        # TODO - Create a new annotation in the database with the given details
        # TODO - Broadcast the new annotation to all clients viewing the same document
        pass

    @socketio.on('update_annotation')
    def handle_update_annotation(data):
        # TODO - Confirm user permissions to ensure they can update the annotation
        # TODO - Find the annotation by ID provided in data
        # TODO - Update the annotation details (e.g., content, position) and save changes
        # TODO - Broadcast the updated annotation details to all clients subscribed to the document
        pass

    @socketio.on('delete_annotation')
    def handle_delete_annotation(data):
        # TODO - Verify the user's permission to delete the annotation
        # TODO - Locate the annotation by its ID and delete it from the database
        # TODO - Notify all clients viewing the document that the annotation has been deleted
        pass
