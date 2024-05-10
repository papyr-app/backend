import logging
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from file_manager.ifile_manager import IFileManager


class S3Client(IFileManager):
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_file(self, source, destination):
        try:
            self.s3_client.upload_file(source, self.bucket_name, destination)
            logging.info(f"File {source} uploaded to {self.bucket_name}/{destination}")
        except NoCredentialsError:
            logging.error("Credentials not available")
        except ClientError as e:
            logging.error(f"Error uploading file: {e}")

    def download_file(self, source, destination):
        try:
            self.s3_client.download_file(self.bucket_name, source, destination)
            logging.info(f"File {source} downloaded to {destination}")
        except NoCredentialsError:
            logging.error("Credentials not available")
        except ClientError as e:
            logging.error(f"Error downloading file: {e}")

    def delete_file(self, file_path):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_path)
            logging.info(f"File {file_path} deleted from {self.bucket_name}")
        except NoCredentialsError:
            logging.error("Credentials not available")
        except ClientError as e:
            logging.error(f"Error deleting file: {e}")

    def list_files(self, prefix=''):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            return [item['Key'] for item in response.get('Contents', [])]
        except NoCredentialsError:
            logging.error("Credentials not available")
        except ClientError as e:
            logging.error(f"Error listing files: {e}")
            return []
