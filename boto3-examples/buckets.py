import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name):
    """
    Create a bucket with a specified name
    :param bucket_name:
    :return: False if ClientError is encountered, otherwise True
    """
    session = boto3.session.Session()
    try:
        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        s3.create_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        print(e.with_traceback(None))
        return False


def list_buckets():
    """
    List existing buckets in the cloud
    :return: False if ClientError is encountered, otherwise True
    """
    session = boto3.session.Session()
    try:
        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        buckets = s3.list_buckets()
        for bucket in buckets['Buckets']:
            print(bucket['Name'] + '\n')
        return True
    except ClientError as e:
        print(e.with_traceback(None))
        return False


if __name__ == '__main__':
    # create_bucket("pr22-09-test-bucket")
    list_buckets()
