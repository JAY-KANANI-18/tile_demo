import os 
from services.aws import AWSS3Service 
import chardet
import io

aws_access_key_id = 'AKIA36AHESWZI7QE4N7H'
aws_secret_access_key = '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'
# aws_secret_access_key = 'GUj2rOeT0wDmIsbWfgTAYe0nW5kOZGSfabP7QVh9'
s3_service = AWSS3Service(aws_access_key_id, aws_secret_access_key)




def image_data_with_features_pkl(model_name):
    image_data_with_features_pkl= s3_service.read_file_from_s3(f"{model_name}/meta/image_data_features.pkl")

    return image_data_with_features_pkl

def image_features_vectors_idx(model_name):
    image_features_vectors_idx = s3_service.read_file_from_s3(f"{model_name}/meta/image_features_vectors.idx")
 

    return (image_features_vectors_idx)


# def image_data_with_features_pkl(model_name):
#     image_data_with_features_pkl = os.path.join('metadata-files/',f'{model_name}/','image_data_features.pkl')
#     return image_data_with_features_pkl

# def image_features_vectors_idx(model_name):
#     image_features_vectors_idx = os.path.join('metadata-files/','vgg19','image_features_vectors.idx')
#     return image_features_vectors_idx
