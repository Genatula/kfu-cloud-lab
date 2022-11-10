import boto3
import requests
from botocore.exceptions import ClientError


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


if __name__ == '__main__':
    url = create_presigned_url('pr22-09-test-bucket', '1.png')
    response = requests.get(url)
    with open('../assets/presigned_1.png', 'wb') as image:
        image.write(response.content)
