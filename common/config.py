import uuid

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import mimetypes


def get_content_type(file_name):
    content_type, _ = mimetypes.guess_type(file_name)
    if not content_type:
        return 'application/octet-stream'
    return content_type


def get_file_extension(file_name):
    return mimetypes.guess_extension(file_name)


def get_allowed_content_type(file_name):
    content_type = get_content_type(file_name)

    if content_type.startswith('image/') or content_type.startswith('video/'):
        return content_type
    else:
        raise ValueError("지원되지 않는 파일 형식입니다.")


def create_presigned_url(user_id, post_id, file_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME
    )
    try:
        content_type = get_content_type(file_name)
        file_extension = get_file_extension(file_name)
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': settings.AWS_S3_BUCKET_NAME,
                    'Key': f'{user_id}/{post_id}/{unique_filename}',
                    'ContentType': content_type
                    },
            ExpiresIn=settings.EXPIRATION)
        return presigned_url
    except ClientError as e:
        return None
