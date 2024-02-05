import boto3
from botocore.exceptions import NoCredentialsError
from botocore.client import Config

class AWSS3Service:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.s3 = boto3.client('s3', region_name='ap-south-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,config=Config(signature_version='s3v4'))

    def list_buckets(self):
        try:
            response = self.s3.list_buckets()
            return [bucket['Name'] for bucket in response['Buckets']]
        except NoCredentialsError:
            print("Credentials not available")

    # def create_bucket(self, bucket_name):
    #     try:
    #         self.s3.create_bucket(Bucket=bucket_name)
    #         print(f"Bucket '{bucket_name}' created successfully.")
    #     except NoCredentialsError:
    #         print("Credentials not available")

    def upload_file(self, file_path, bucket_name, object_key):
        try:
            self.s3.upload_file(file_path, bucket_name, object_key)
            print(f"File '{object_key}' uploaded to '{bucket_name}' successfully.")
        except NoCredentialsError:
            print("Credentials not available")

    def download_file(self, bucket_name, object_key, download_path):
        try:
            self.s3.download_file(bucket_name, object_key, download_path)
            print(f"File '{object_key}' downloaded to '{download_path}' successfully.")
        except NoCredentialsError:
            print("Credentials not available")

    def list_objects(self, bucket_name):
        try:
            response = self.s3.list_objects(Bucket=bucket_name)
            return [obj['Key'] for obj in response.get('Contents', [])]
        except NoCredentialsError:
            print("Credentials not available")

    def delete_object(self, bucket_name, object_key):
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=object_key)
            print(f"Object '{object_key}' deleted from '{bucket_name}' successfully.")
        except NoCredentialsError:
            print("Credentials not available")

    def delete_bucket(self, bucket_name):
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' deleted successfully.")
        except NoCredentialsError:
            print("Credentials not available")
    def generate_presigned_url(self, bucket_name, object_key, expiration_time=3600):
        try:
            url = self.s3.generate_presigned_url(
                'put_object',
                Params={'Bucket': bucket_name, 'Key': object_key},
                ExpiresIn=expiration_time
            )
            return url
        except NoCredentialsError:
            print("Credentials not available")

# Example Usage:
# aws_access_key_id = 'your_access_key'
# aws_secret_access_key = 'your_secret_key'

# s3_service = AWSS3Service(aws_access_key_id, aws_secret_access_key)

# buckets = s3_service.list_buckets()
# print("Buckets:", buckets)

# new_bucket_name = 'your-unique-bucket-name'
# s3_service.create_bucket(new_bucket_name)

# file_path_to_upload = 'path/to/your/file.txt'
# object_key_to_upload = 'file.txt'
# s3_service.upload_file(file_path_to_upload, new_bucket_name, object_key_to_upload)

# download_path = 'path/to/save/downloaded/file.txt'
# s3_service.download_file(new_bucket_name, object_key_to_upload, download_path)

# objects_in_bucket = s3_service.list_objects(new_bucket_name)
# print("Objects in bucket:", objects_in_bucket)

# s3_service.delete_object(new_bucket_name, object_key_to_upload)

# s3_service.delete_bucket(new_bucket_name)
