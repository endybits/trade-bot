import os
import boto3
from botocore.exceptions import ClientError

from app.config.fconfig import get_aws_s3_info

s3_info = get_aws_s3_info()
BUCKET = s3_info.get('bucket_name')
REGION = s3_info.get('region')
def uploadFileToS3(path, filename):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: file_url if file was uploaded, else None
    """
    s3_client = boto3.client('s3')
    file_path = os.path.join(path, filename)
    try:
        s3_client.upload_file(file_path, BUCKET, filename)
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET, 'Key': filename},
            ExpiresIn=3600
            )
        print(url)
        #file_url = f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{filename}"
        return url
    except ClientError as e:
        print(f"Error: {e}")
        return f"Error: {e}"