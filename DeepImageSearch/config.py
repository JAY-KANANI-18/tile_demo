import os 
from services.aws import AWSS3Service 
import chardet
import io

aws_access_key_id = 'AKIA36AHESWZI7QE4N7H'
aws_secret_access_key = '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'
# aws_secret_access_key = 'GUj2rOeT0wDmIsbWfgTAYe0nW5kOZGSfabP7QVh9'
s3_service = AWSS3Service(aws_access_key_id, aws_secret_access_key)




def image_data_with_features_pkl(model_name):
    try:
     image_data_with_features_pkl= s3_service.read_file_from_s3(f"{model_name}/meta/image_data_features.pkl",f"{model_name}.pkl")

     return image_data_with_features_pkl
    except Exception as e:
        print(e)


def image_features_vectors_idx(model_name):
    try:
     image_features_vectors_idx = s3_service.read_file_from_s3(f"{model_name}/meta/image_features_vectors.idx",f"{model_name}.idx")
 

     return (image_features_vectors_idx)
    except Exception as e:
       print(e)


def image_data_with_features_pk_local(model_name):
    try:
     image_data_with_features_pkl = os.path.join('metadata-files/',f'{model_name}/','image_data_features.pkl')
     return image_data_with_features_pkl
    except Exception as e:
      print(e)

def image_features_vectors_idx_local(model_name):
  try:
    image_features_vectors_idx = os.path.join('metadata-files/','vgg19','image_features_vectors.idx')
    return image_features_vectors_idx
  except Exception as e:
      print(e)