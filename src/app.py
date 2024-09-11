import json
import boto3
import os
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        content_type = event['headers'].get('Content-Type', 'application/octet-stream')
        body = event['body']
        if event.get('isBase64Encoded', False):
            import base64
            body = base64.b64decode(body)

        file_name = str(uuid.uuid4()) + ".jpg"
        

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f'images/{file_name}',
            Body=body,
            ContentType=content_type
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Image uploaded successfully', 
                'file_name': file_name})
        }
    except Exception as e:
        print(e) 
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)})
        }
