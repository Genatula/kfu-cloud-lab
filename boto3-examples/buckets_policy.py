import boto3
from botocore.exceptions import ClientError
import json


def get_policy(bucket):
    session = boto3.session.Session()
    try:
        client = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        result = client.get_bucket_policy(Bucket=bucket)
    except ClientError as e:
        print(e.with_traceback(None))
        result = {'Policy': None}
    return result['Policy']


def set_granting_policy(bucket):
    bucket_policy = {
        'Version': '2022-11-14',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:getObject']
        }]
    }
    bucket_policy = json.dumps(bucket_policy)
    session = boto3.session.Session()
    try:
        client = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        client.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)
        return True
    except ClientError as e:
        print(e.with_traceback(None))
        return False


def delete_bucket_policy(bucket):
    session = boto3.session.Session()
    try:
        client = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        client.delete_bucket_policy(Bucket=bucket)
        return True
    except ClientError as e:
        print(e.with_traceback(None))
        return False


if __name__ == '__main__':
    set_granting_policy('pr22-09-test-bucket')
    print(get_policy('pr22-09-test-bucket'))
    delete_bucket_policy('pr22-09-test-bucket')
    print(get_policy('pr22-09-test-bucket'))
