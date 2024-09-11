import json
import boto3
import os
import base64

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    file_name = event['pathParameters']['file_name']
    s3_key = f'images/{file_name}'

    try:
        # Get the object from S3
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        file_content = response['Body'].read()

        # Return the file content as a base64-encoded string
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': response['ContentType'],
                'Content-Disposition': f'attachment; filename="{file_name}"'
            },
            'body': base64.b64encode(file_content).decode('utf-8'),
            'isBase64Encoded': True
        }
    except s3_client.exceptions.NoSuchKey:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'File not found'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }