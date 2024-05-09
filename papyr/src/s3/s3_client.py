import logging
import boto3
from botocore.exceptions import NoCredentialsError, ClientError


class S3Client:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_file(self, file, filename):
        try:
            self.s3.upload_fileobj(file, self.bucket_name, filename)
            return f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
        except (NoCredentialsError, ClientError) as e:
            logging.error(e)
            return None

    def download_file(self, filename):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=filename)
            return response['Body']
        except (NoCredentialsError, ClientError) as e:
            logging.error(e)
            return None

    def delete_file(self, filename):
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=filename)
        except (NoCredentialsError, ClientError) as e:
            logging.error(e)
            return None
