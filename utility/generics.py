import uuid

from boto3 import Session
from django.conf import settings


def upload_file_to_s3(file, file_name):
    """
    Upload file to amazon s3
    :param file: InMemoryUploadedFile instance
    :param file_name:
    :return:
    """
    session = Session(aws_access_key_id=settings.S3_ACCESS_KEY,
                      aws_secret_access_key=settings.S3_SECRET_KEY)
    _s3 = session.resource("s3")

    s3_upload_path = str(uuid.uuid4()) + file_name
    _s3.Bucket("nexinvent").put_object(Key=s3_upload_path, Body=file)
    url = "https://s3.ap-south-1.amazonaws.com/nexinvent/" + s3_upload_path
    return url


