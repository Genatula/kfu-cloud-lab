import boto3
import os
from botocore.exceptions import ClientError


class FileUploadNotifier(object):

    def __init__(self, filename):
        self._filename = filename

    def __call__(self, bytes_amount):
        print("%r bytes of %s has been uploaded" % (bytes_amount, os.path.basename(self._filename)))


def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file with the specified name to a bucket and save it with the specified name
    :param file_name: Path to a file
    :param bucket: Name of a bucket
    :param object_name: Name of an object
    :return: False if ClientError is encountered, otherwise True
    """
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


def download_file(bucket, object_name, file_name):
    """
    Download an object with the specified name from a bucket and save it with the specified name
    :param bucket: name of a bucket
    :param object_name: name of an object within the bucket
    :param file_name: name of a file to which save the object
    :return: False if ClientError is encountered, otherwise True
    """
    try:
        session = boto3.session.Session()
        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        s3.download_file(bucket, object_name, file_name)
        return True
    except ClientError as e:
        print(e.with_traceback(None))
        return False


if __name__ == '__main__':
    # upload_file('../assets/1.png', 'pr22-09-test-bucket')
    download_file('pr22-09-test-bucket', '1.png', '../assets/downloaded_1.png')
