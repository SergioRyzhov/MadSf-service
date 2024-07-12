from urllib.parse import urljoin

import boto3
from botocore.client import Config
from app.config import settings

s3_client = boto3.client(
    's3',
    endpoint_url=settings.S3_ENDPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    config=Config(signature_version='s3v4')
)


def upload_image(file, filename):
    image_url = urljoin('http://minio:9000/memes/', filename)
    return str(image_url)
