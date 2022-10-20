import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig, MB
import os


def upload_file_with_custom_config(bucket_name, file_name, object_name=None):
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        if object_name is None:
            object_name = os.path.basename(file_name)
        transfer_config = TransferConfig(multipart_threshold=2 * MB, max_concurrency=5)
        client.upload_file(file_name, bucket_name, object_name, Config=transfer_config)
        return True
    except ClientError as e:
        print(e.with_traceback(None))
        return False


if __name__ == '__main__':
    upload_file_with_custom_config('pr22-09-test-bucket', '../assets/02.png')
