from flask import request, jsonify, send_file, Blueprint
from io import BytesIO
from s3.s3_client import S3Client


def create_file_blueprint(s3_client: S3Client) -> Blueprint:
    file_bp = Blueprint('file', __name__, url_prefix='/api/files')

    @file_bp.route('/upload', methods=['POST'])
    def upload():
        file = request.files['file']
        filename = file.filename
        s3_url = s3_client.upload_file(file, filename)
        if s3_url:
            return jsonify({'url': s3_url}), 201
        else:
            return jsonify({'error': 'Upload failed'}), 500

    @file_bp.route('/download/<filename>', methods=['GET'])
    def download(filename):
        file_stream = s3_client.download_file(filename)
        if file_stream:
            return send_file(BytesIO(file_stream.read()), attachment_filename=filename, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404

    @file_bp.route('/delete/<filename>', methods=['DELETE'])
    def delete(filename):
        if s3_client.delete_file(filename):
            return jsonify({'message': 'File deleted successfully'}), 200
        else:
            return jsonify({'error': 'Deletion failed'}), 500

    return file_bp
