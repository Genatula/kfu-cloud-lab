import boto3
import requests
from botocore.exceptions import ClientError
from files import download_file


def create_presigned_url(bucket, object_name, expiration_time=3600):
    session = boto3.session.Session()
    client = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    try:
        server_response = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket,
                'Key': object_name
            },
            ExpiresIn=expiration_time
        )
    except ClientError as e:
        print(e.with_traceback(None))
        server_response = None
    return server_response


def create_presigned_post(bucket, object_name, ttl=3600, fields=None, conditions=None):
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        server_response = client.generate_presigned_post(
            bucket, object_name, Fields=fields, Conditions=conditions, ExpiresIn=ttl
        )
    except ClientError as e:
        print(e.with_traceback(None))
        server_response = None
    finally:
        return server_response


if __name__ == '__main__':
    url = create_presigned_url('pr22-09-test-bucket', '1.png')
    response = requests.get(url)
    with open('../assets/presigned_1.png', 'wb') as image:
        image.write(response.content)
    post_url_response = create_presigned_post('pr22-09-test-bucket', 'presigned_02.png')
    with open('../assets/02.png', 'rb') as image:
        files = {'file': ('presigned_02.png', image)}
        response = requests.post(post_url_response['url'], data=post_url_response['fields'], files=files)
    print(response.status_code)
    download_file('pr22-09-test-bucket', 'presigned_02.png', '../assets/presigned_02.png')
