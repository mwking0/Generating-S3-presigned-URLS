import json
import boto3

def lambda_handler(event, context):
    bucket_name = 'your-bucket-name'
    object_key = 'your-object-key'
    pre_signed_url = generate_presigned_url(bucket_name, object_key)

    if pre_signed_url:
        print(f"Pre-signed URL for '{object_key}':\n{pre_signed_url}")
        send_presigned_url(pre_signed_url)
    else:
        print("Failed to generate pre-signed URL.")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def send_presigned_url(pre_signed_url):
    message = {"foo": "bar"}
    client = boto3.client('sns')
    response = client.publish(
        TargetArn='your-sns-topic-arn',
        Message=json.dumps({'default': json.dumps(pre_signed_url)}),
        Subject='Presigned URL',
        MessageStructure='json'
    )

def generate_presigned_url(bucket_name, object_key, expiration_time=3600):
    s3_client = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'), region_name='us-east-1')

    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration_time
        )

        return presigned_url

    except Exception as ex:
        print("Exception occurred:", ex)
        return None
