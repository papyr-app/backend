import os
from flask import request, jsonify, send_file, Blueprint
from file_manager.s3_client import S3Client
from werkzeug.utils import secure_filename

from auth.decorators import token_required
from models.user import User


def create_file_blueprint(s3_client: S3Client) -> Blueprint:
    file_bp = Blueprint('file', __name__, url_prefix='/api/files')

    @file_bp.route('/upload', methods=['POST'])
    @token_required
    def upload(user: User):
        file = request.files.get('file')
        path = request.form.get('path', '')

        if not file:
            return jsonify({'error': 'Missing required fields'}), 400

        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400

        username = user.username
        secure_name = secure_filename(file.filename)
        key = f"{username}/{path}/{secure_name}".strip('/')

        if s3_client.file_exists(key):
            return jsonify({'error': 'File already exists'}), 400

        upload_succeeded = s3_client.upload_file(file, key)
        if upload_succeeded:
            return jsonify({'success': 'Uploaded file'}), 201
        else:
            return jsonify({'error': 'Upload failed'}), 500

    @file_bp.route('/download/<path:path>', methods=['GET'])
    @token_required
    def download(user: User, path: str):
        # TODO - authenticate that the user is allowed to download this file
        username = user.username
        key = f"{username}/{path}".strip('/')
        filename = os.path.basename(path)

        if not s3_client.file_exists(key):
            return jsonify({'error': 'File not found'}), 404

        file_stream = s3_client.download_file(key)
        if not file_stream:
            return jsonify({'error': 'File not found'}), 404

        return send_file(
            file_stream,
            download_name=filename,
            as_attachment=True
        )

    @file_bp.route('/delete/<path:path>', methods=['DELETE'])
    @token_required
    def delete(user: User, path: str):
        username = user.username
        key = f"{username}/{path}".strip('/')

        if not s3_client.file_exists(key):
            return jsonify({'error': 'File not found'}), 404

        if s3_client.delete_file(key):
            return jsonify({'data': 'File deleted successfully'}), 200
        else:
            return jsonify({'error': 'Deletion failed'}), 500

    return file_bp
