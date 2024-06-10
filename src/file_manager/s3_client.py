import logging
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from file_manager.ifile_manager import IFileManager


class S3Client(IFileManager):
    def __init__(self, bucket_name):
        self.s3 = boto3.client("s3")
        self.bucket_name = bucket_name

    def upload_file(self, file: BytesIO, path: str) -> bool:
        try:
            self.s3.upload_fileobj(file, self.bucket_name, path)
            logging.info(f"File uploaded to {self.bucket_name}/{path}")
            return True
        except NoCredentialsError:
            logging.error("Credentials not available")
            return False
        except ClientError as e:
            logging.error(f"Error uploading file: {e}")
            return False

    def download_file(self, path: str) -> BytesIO:
        try:
            buffer = BytesIO()
            self.s3.download_fileobj(self.bucket_name, path, buffer)
            logging.info(f"File downloaded from {self.bucket_name}/{path}")
            buffer.seek(0)
            return buffer
        except NoCredentialsError:
            logging.error("Credentials not available")
            return None
        except ClientError as e:
            logging.error(f"Error downloading file: {e}")
            return None

    def delete_file(self, path: str) -> bool:
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=path)
            logging.info(f"File deleted from {self.bucket_name}/{path}")
            return True
        except NoCredentialsError:
            logging.error("Credentials not available")
            return False
        except ClientError as e:
            logging.error(f"Error deleting file: {e}")
            return False

    def file_exists(self, path: str) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=path)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                raise e
