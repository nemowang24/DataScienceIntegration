import boto3

s3_client = boto3.client('s3')

bucket_name = 'webserver-private'
pdf_key = 'churnanalysishomework.pdf'

# Generate a pre-signed URL (valid for 1 hour)
url = s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': pdf_key},
    ExpiresIn=3600
)

print("Presigned URL:", url)
