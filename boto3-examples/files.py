import boto3
import os
from botocore.exceptions import ClientError


class FileUploadNotifier(object):

    def __init__(self, filename):
        self._filename = filename

    def __call__(self, bytes_amount):
        print("%r bytes of %s has been uploaded" % (bytes_amount, os.path.basename(self._filename)))


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        session = boto3.session.Session()
        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        response = s3.upload_file(file_name, bucket, object_name, Callback=FileUploadNotifier(file_name))
        return True
    except ClientError as e:
        print(e.with_traceback(None))
        return False


if __name__ == '__main__':
    upload_file('../assets/1.png', 'pr22-09-test-bucket')
