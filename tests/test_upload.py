import json
import boto3
from moto import mock_s3
import pytest
from src.app import lambda_handler
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_s3_client():
    with mock_s3():
        s3_client = boto3.client('s3')
        bucket_name = 'my-app-users-s3-bucket'
        s3_client.create_bucket(Bucket=bucket_name)
        yield s3_client

@pytest.fixture
def set_env_vars():
    with patch.dict('os.environ', {'BUCKET_NAME': 'my-app-users-s3-bucket'}):
        yield

def test_successful_image_upload(mock_s3_client, set_env_vars):
    event = {
        'headers': {
            'Content-Type': 'image/jpeg'
        },
        'body': 'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxYAAAABJRU5ErkJggg==',  # Base64 for a 1x1 PNG image
        'isBase64Encoded': True
    }
    context = {}
    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['message'] == 'Image uploaded successfully'
    assert 'file_name' in body
    assert response['body'] is not None


def test_upload_failure(mock_s3_client, set_env_vars):
    with patch('boto3.client') as mock_boto_client:
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = Exception('Upload failed')
        mock_boto_client.return_value = mock_s3
        
        event = {
            'headers': {
                'Content-Type': 'image/jpeg'
            },
            'body': 'iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxYAAAABJRU5ErkJggg==',
            'isBase64Encoded': True
        }
        context = {}
        response = lambda_handler(event, context)

        assert response['statusCode'] == 500
        body = json.loads(response['body'])
        assert body['message'] == 'Internal Server Error'
        assert 'error' in body