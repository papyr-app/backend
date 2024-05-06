import logging
from flask_socketio import emit, join_room, leave_room

from models.annotation import Annotation


def handle_annotations(socketio):
    @socketio.on('fetch_current_annotations')
    def fetch_current(data):
        document_id = data['document_id']
        annotations = Annotation.objects(document_id=document_id)
        annotations_data = [{'id': str(ann.id), 'content': ann.content} for ann in annotations]
        emit('current_annotations', annotations_data, room=request.sid)

    @socketio.on('create_comment')
    def handle_create_comment(data):
        # Extract information from data (assuming data includes annotation_id, user_id, and content)
        # Create a new comment in the database
        # Notify all clients that are subscribed to updates for this annotation
        pass

    @socketio.on('update_comment')
    def handle_update_comment(data):
        # Check user permissions to ensure they can update the comment
        # Find the comment by ID, update its content, and save the changes
        # Broadcast the updated comment to all clients viewing the same annotation
        pass

    @socketio.on('delete_comment')
    def handle_delete_comment(data):
        # Verify user permission to delete the comment
        # Locate the comment by ID and delete it from the database
        # Inform all clients viewing the annotation of the comment deletion
        pass

    @socketio.on('create_annotation')
    def handle_create_annotation(data):
        # Extract necessary information from data, such as the content of the annotation, the page number, and user_id
        # Create a new annotation in the database with the given details
        # Broadcast the new annotation to all clients viewing the same document
        # Ensure to include information like annotation ID, content, and page number in the broadcast
        pass

    @socketio.on('update_annotation')
    def handle_update_annotation(data):
        # Confirm user permissions to ensure they can update the annotation
        # Find the annotation by ID provided in data
        # Update the annotation details (e.g., content, position) and save changes
        # Broadcast the updated annotation details to all clients subscribed to the document
        pass

    @socketio.on('delete_annotation')
    def handle_delete_annotation(data):
        # Verify the user's permission to delete the annotation
        # Locate the annotation by its ID and delete it from the database
        # Notify all clients viewing the document that the annotation has been deleted
        pass

