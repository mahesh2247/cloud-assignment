import json
import boto3
import os
from PIL import Image
import io

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # Parse the S3 event
        records = event.get('Records', [])
        for record in records:
            s3_bucket = record['s3']['bucket']['name']
            s3_key = record['s3']['object']['key']
            
            # Check if the file is in the 'images/' folder
            if s3_key.startswith('images/'):
                # Download the image
                response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
                image_content = response['Body'].read()
                
                # Open the image
                image = Image.open(io.BytesIO(image_content))
                
                # Create a thumbnail
                thumbnail = image.copy()
                thumbnail.thumbnail((100, 100))  # Adjust the size as needed
                
                thumbnail_io = io.BytesIO()
                thumbnail.save(thumbnail_io, format='JPEG')
                thumbnail_io.seek(0)
                
                thumbnail_key = s3_key.replace('images/', 'thumbnail/')
                s3.put_object(
                    Bucket=s3_bucket,
                    Key=thumbnail_key,
                    Body=thumbnail_io.getvalue(),
                    ContentType='image/jpeg'
                )
                
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Thumbnail created successfully'})
        }
    except Exception as e:
        print(e) 
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)})
        }
