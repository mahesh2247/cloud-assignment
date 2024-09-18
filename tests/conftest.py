from dotenv import load_dotenv
import os
import pytest, moto, boto3
from moto import mock_s3

def pytest_configure():
    load_dotenv()

@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@mock_s3
@pytest.fixture
def mock_s3_client(aws_credentials):
    # moto_fake = moto.mock_s3()
    # try:
    #     moto_fake.start()
    #     conn = boto3.resource('s3')
    #     conn.create_bucket(Bucket="my-app-users-s3-bucket-dev")  # or the name of the bucket you use
    #     yield conn
    # finally:
    #     moto_fake.stop()
    with moto.mock_s3():
        s3_client = boto3.client('s3', region_name='us-east-1')
        bucket_name = "my-app-users-s3-bucket"
        s3_client = s3_client.create_bucket(Bucket=bucket_name)
        yield s3_client
