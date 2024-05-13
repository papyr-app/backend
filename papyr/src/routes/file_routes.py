from flask import request, jsonify, send_file, Blueprint
from file_manager.s3_client import S3Client


def create_file_blueprint(s3_client: S3Client) -> Blueprint:
    file_bp = Blueprint('file', __name__, url_prefix='/api/files')

    @file_bp.route('/upload', methods=['POST'])
    def upload():
        # TODO
        # 0. If the file is not PDF, return error
        # 1. get the username from the JWT
        # 2. construct a key that looks like this: username/path/title
        # 3. check if file path already exists, if it does return error
        # 4. otherwise upload the file
        file = request.files['file']
        filename = file.filename
        upload_succeeded = s3_client.upload_file(file, filename)
        if upload_succeeded:
            return jsonify({'success': 'Uploaded file'}), 201
        else:
            return jsonify({'error': 'Upload failed'}), 500

    @file_bp.route('/download/<filename>', methods=['GET'])
    def download(filename):
        # TODO
        # 1. get the username from the JWT
        # 2. construct a file_path that looks like this username/file_path
        # 3. check if that file path already exists, if it doesnt return error
        # 4. otherwise download the file
        # 5. return the downloaded file
        file = s3_client.download_file(filename)
        if file:
            return send_file(file, download_name=filename, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404

    @file_bp.route('/delete/<filename>', methods=['DELETE'])
    def delete(filename):
        # TODO
        # 1. get the username from the JWT
        # 2. construct a file_path that looks like this username/file_path
        # 3. check if that file path already exists, if it doesnt return error
        # 4. otherwise delete the file
        if s3_client.delete_file(filename):
            return jsonify({'message': 'File deleted successfully'}), 200
        else:
            return jsonify({'error': 'Deletion failed'}), 500

    return file_bp
