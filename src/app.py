# import json
# import base64
# import boto3
# import os
# import uuid

# # Initialize the S3 client
# s3 = boto3.client('s3')

# # Get the bucket name from environment variables
# BUCKET_NAME = os.environ['BUCKET_NAME']

# def lambda_handler(event, context):
#     try:
#         # Log the incoming event for debugging
#         print(f"Event: {json.dumps(event)}")

#         # Check if the body is empty
#         if not event.get('body'):
#             return {
#                 'statusCode': 400,
#                 'body': json.dumps({'message': 'No file content provided'}),
#                 'headers': {'Content-Type': 'application/json'}
#             }

#         # Extract the file name from headers
#         file_name = event['headers'].get('file_name', 'uploaded_image.jpg')

#         # Check if the request body is base64 encoded
#         is_base64_encoded = event.get('isBase64Encoded', False)
        
#         # Decode the body if it is base64 encoded
#         if is_base64_encoded:
#             file_content = base64.b64decode(event['body'])
#         else:
#             file_content = event['body']
        
#         # Generate a unique file name (optional)
#         unique_file_name = f"{uuid.uuid4()}-{file_name}"

#         # Upload the image to the S3 bucket
#         s3.put_object(
#             Bucket=BUCKET_NAME,
#             Key=f'image/{unique_file_name}',
#             Body=file_content,
#             ContentType=event['headers'].get('Content-Type', 'image/jpeg')  # MIME type
#         )

#         return {
#             'statusCode': 200,
#             'body': json.dumps({
#                 'message': 'File uploaded successfully!',
#                 'file_name': unique_file_name
#             }),
#             'headers': {'Content-Type': 'application/json'}
#         }

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'error': str(e)}),
#             'headers': {'Content-Type': 'application/json'}
#         }


import json
import boto3
import os
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # Extract the image file from the event
        content_type = event['headers'].get('Content-Type', 'application/octet-stream')
        body = event['body']
        if event.get('isBase64Encoded', False):
            import base64
            body = base64.b64decode(body)
        
        # Generate a unique file name
        file_name = str(uuid.uuid4()) + ".jpg"  # Adjust as needed
        
        # Upload the image to the 'images/' folder in the S3 bucket
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f'images/{file_name}',
            Body=body,
            ContentType=content_type
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Image uploaded successfully'})
        }
    except Exception as e:
        print(e)  # Log the error for debugging
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)})
        }
