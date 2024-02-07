import io
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.client import Config

class AWSS3Service:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.s3 = boto3.client('s3', region_name='ap-south-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,config=Config(signature_version='s3v4'))

    def list_buckets(self):
        try:
            response = self.s3.list_buckets() 
            print(response)
            return [bucket['Name'] for bucket in response['Buckets']]
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
    def generate_get_presigned_url(self, bucket_name, object_key, expiration_time=3600):
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_key},
                ExpiresIn=expiration_time
            )
            return url
        except NoCredentialsError:
            print("Credentials not available")

    def create_bucket(self, bucket_name):
        try:
            self.s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        except NoCredentialsError:
            print("Credentials not available")

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
    
    def read_file_from_s3(self,file_path,local_path="file"):
     try:

      local_file_name = f'test/{local_path}'
      response = self.s3.download_file("designfinder", file_path,local_file_name)

      print(response)
    #   if not response:
    #       source_path = "metadata-files\vgg19\image_data_features.pkl"
    #       source_path1 = "metadata-files\vgg19\image_features_vectors.idx"
    #       destination_path = local_path
    #       destination_path1 = f"test/{}"
    #       with open(source_path, 'rb') as source_file:
    # # Open the destination file for writing in binary mode
    #          with open(destination_path, 'wb') as destination_file:
    #     # Read the content of the source file and write it to the destination file
    #             destination_file.write(source_file.read())

    #       print(f"File copied from {source_path} to {destination_path}")
          
        
          
      
    #  file_content = response['Body'].read()
      return local_file_name
     except Exception as e:
       print(e)
