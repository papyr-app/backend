import logging
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from src.file_manager.ifile_manager import IFileManager


class S3Client(IFileManager):
    def __init__(self, bucket_name):
        self.s3 = boto3.client("s3")
        self.bucket_name = bucket_name

    def upload_file(self, file: BytesIO, path: str) -> bool:
        try:
            self.s3.upload_fileobj(file, self.bucket_name, path)
            logging.debug("File uploaded to %s/%s", self.bucket_name, path)
            return True
        except NoCredentialsError:
            logging.error("Credentials not available")
            return False
        except ClientError as e:
            logging.error("Error uploading file: %s", e)
            return False

    def download_file(self, path: str) -> BytesIO:
        try:
            buffer = BytesIO()
            self.s3.download_fileobj(self.bucket_name, path, buffer)
            logging.debug("File downloaded from %s/%s", self.bucket_name, path)
            buffer.seek(0)
            return buffer
        except NoCredentialsError:
            logging.error("Credentials not available")
            return None
        except ClientError as e:
            logging.error("Error downloading file: %s", e)
            return None

    def delete_file(self, path: str) -> bool:
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=path)
            logging.debug("File deleted from %s/%s", self.bucket_name, path)
            return True
        except NoCredentialsError:
            logging.error("Credentials not available")
            return False
        except ClientError as e:
            logging.error("Error deleting file: %s", e)
            return False

    def file_exists(self, path: str) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=path)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise e
