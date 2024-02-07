import io
import os
from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from DeepImageSearch import Load_Data,Search_Setup
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from fileinput import filename 
import json
import pickle
import zipfile
from services.aws import AWSS3Service 
import bcrypt
from bson import ObjectId

aws_access_key_id = 'AKIA36AHESWZI7QE4N7H'
aws_secret_access_key = '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'
# aws_secret_access_key = 'GUj2rOeT0wDmIsbWfgTAYe0nW5kOZGSfabP7QVh9'
s3_service = AWSS3Service(aws_access_key_id, aws_secret_access_key)

import time
import random

def generate_unique_token():
    timestamp = int(time.time() * time.time())  # Get current time in milliseconds
    random_part = random.randint(0, 9999)  # Add a random component
    token = f"{timestamp:013d}{random_part:04d}"
    return token




# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("./key.json")
# firebase_admin.initialize_app(cred)

# from sklearn.metrics.pairwise import cosine_similarity

# class TT:

#  def get_similar_images(self, image_path: str, number_of_images: int = 10):
#   self.image_path = image_path
#   self.number_of_images = number_of_images
#   query_vector = self._get_query_vector(self.image_path)
#   img_dict = self._search_by_vector(query_vector, self.number_of_images)
#  # Calculate similarity percentages
#   similarity_percentages = []
#   for img_path in img_dict.values():
#    img_vector = self._get_query_vector(img_path)
#    similarity = cosine_similarity([query_vector], [img_vector])[0][0]
#    similarity_percentages.append(similarity)
#   return img_dict, similarity_percentages

from pymongo import MongoClient
from pymongo.server_api import ServerApi


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def remove_files(file_path):
    if os.path.exists(file_path):
         os.remove(file_path)
         print(f"{file_path} removed successfully")
    else:
        print(f"The file {file_path} does not exist")
        return jsonify({"success":True,"msg":"Image add successfully"})


mongo_url = "mongodb+srv://revotechsolution23:FUATSOzYa2zzV1wp@cluster0.ps9gbjq.mongodb.net/"  # MongoDB connection URL
database_name = "DESIGN_FINDER"  # Your database name



client = MongoClient(mongo_url)
database = client[database_name]


db_names = client.list_database_names()

# If listing database names was successful, log the successful connection
print("Connected to MongoDB. Database names:", db_names)



collection_name = "all_carpets"
collection = database[collection_name]
collection2 = database["metadata"]



image_directory = './main_carpet'
image_names = [filename for filename in os.listdir(image_directory) if filename.endswith(('.jpg', '.png', '.jpeg', '.gif', '.bmp'))]

# for image_name in image_names:
#     database[collection_name].insert_one({"name": image_name})


# with open('./metadata-files/vgg19/image_data_features.pkl','rb') as file :
#     data= pickle.load(file)
#     print('efjefej')
#     collection2.insert_one({"data":data})





app = Flask(__name__)
CORS(app,  resources={r"/*": {"origins": "*"}})
image_list = Load_Data().from_folder(['./main_carpet'])
st = Search_Setup(image_list=image_list, file_path='vgg19', pretrained=True, image_count=1)
st.run_index(True)


@app.before_request
def authenticate():
    try:

    
        excluded_routes = {'login', 'signup', 'logout',"get_image"}

        if request.endpoint and request.endpoint in excluded_routes:
            print(" line 131")
            return 

        user = None

        
        user = database["users"].find_one({"email":request.headers["email"]})

        if user == None:
         print("connd true")
         return jsonify({"sucess":False,"msg":"user not Found"})
        print("cond false")

 
        if "token" not in request.headers or user["token"] != request.headers["token"]:
            return jsonify({"sucess":False,"msg":"Authentication failed"})

       
    except Exception as e :
        print("error")
        print(e)


@app.route('/auth')
def auth():
    user =   database["users"].find_one({"token":request.headers["token"]})
    print(user)
    if(user):
     return jsonify({'status': True})
    else:
     return jsonify({'status': False})


@app.route('/signup',methods=['POST'])
def signup():
    print()

    data = request.get_json()
    print(data)
    duplicate = database['users'].find_one({"email":data["email"]})
    print(duplicate)
    if duplicate != None:
        print(True)
        return jsonify({"status":False,"msg":"email exist"})
    request.json['password'] = hash_password(request.json['password'])
    user = database['users'].insert_one(request.json)
    print()
    s3_service.upload_file("metadata-files/vgg19/image_data_features.pkl","designfinder",f"{user.inserted_id}/meta/image_data_features.pkl")
    s3_service.upload_file("metadata-files/vgg19/image_features_vectors.idx","designfinder",f"{user.inserted_id}/meta/image_features_vectors.idx")

    print('Login called')
    return jsonify({"status":True,"msg":"SignUp Successfull"})


@app.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    print(data)
    user_detail = database['users'].find_one({"email":data["email"]})
    if user_detail == None :
        print('user not register')
        return jsonify({"status":False,"msg":"user not registered"})
    
    res = check_password( data["password"],user_detail['password'] )
    print(res)
    # if user_detail['password'] != data["password"]:
    #     return jsonify({"status":"false","msg":"user name and password didn't match"})
    if not res :
         return jsonify({"status":False,"msg":"user name and password didn't match"})

    token = generate_unique_token()
    database['users'].update_one({"email":data["email"]},{"$set":{"token":token}})
    user_detail["_id"] = str(user_detail["_id"])

    
    return jsonify({"status":True,"msg":"Login Successfull","data":{"token":token,"user":user_detail["_id"]}})


@app.route('/collections/create', methods=['POST'])
def add_collection():
    try:
     
     data = request.get_json()

     collection =  database['collections'].insert_one(request.json)
     print(collection.inserted_id)
     user_detail = database["users"].find_one_and_update(
         {"token": request.headers["token"]},
         {"$push": {"collections":collection.inserted_id}},
         return_document=True 
     )
     return jsonify({"status":True})



    except TypeError as e:
        print("eeeeeeeeeeeeeee")
        print(e)

     
@app.route('/collections', methods=['POST'])
def get_collections_list():
    try:
     print(request.headers["token"] )
     token = request.headers["token"]
     pipeline = [ 
         {"$match" : {"token":token  } },
         {
            "$lookup": {
                "from": "collections",
                "localField": "collections",
                "foreignField": "_id",
                "pipeline":[{"$project":{"_id":0}}],
                "as": "collections"
              }
        },
        {
            "$project":{
                "_id":0,
                "password":0
            }
        }
     ]
     user_detail = list(database["users"].aggregate(pipeline))
     if user_detail:
      print(user_detail)
      return jsonify({"status":True,"data":(user_detail)})
     else:
        return jsonify({"status":False})
    except Exception as e:
        return jsonify({"status":False,"data":None,"error":str(e)})

        print("eeeeeeeeeeeeeee")
        print(e)


@app.route('/collections/details', methods=['POST'])
def collection_details():
    try:
     
     data = request.get_json()

     s =  data["collection_name"]

     collection =  database["collections"].find_one({"name" :s})
     print(collection)
    
     collection['_id'] = str(collection['_id'])
     return jsonify({"status":True,"data":(collection)})



    except Exception as e:
        print("eeeeeeeeeeeeeee")
        print(e)


@app.route('/put_presigned_url', methods=['POST'])
def put_presigned_url():
    data = request.get_json()
    filename = data.get('filename')
    z= s3_service.generate_get_presigned_url("designfinder","meta.pkl",100000)
    print(z)

    presigned_url = s3_service.generate_presigned_url("designfinder",filename,100)
    return jsonify({'presigned_url': presigned_url})


@app.route('/get_presigned_url', methods=['POST'])
def get_presigned_url():
    data = request.get_json()
    filename = data.get('filename')
    # filename = "jay/meta/meta.pkl"
    # filename2 = "jay/meta/meta.idx"


    presigned_url = s3_service.generate_get_presigned_url("designfinder",filename,100000)
    # presigned_url2 = s3_service.generate_get_presigned_url("designfinder",filename2,100000)
    # return jsonify({'presigned_grt_ url': presigned_url,'presigned_grt_ url2': presigned_url2})
    return jsonify({'presigned_grt_ url': presigned_url})


@app.route('/collections/images/add', methods=['POST'])
def add_images():
    try:
     
     data = request.get_json()

     s = ObjectId( data["collection_id"])
     image =data["image"]

     collection =  database["collections"].find_one_and_update({"_id" :s},{"$push":{"images":image}})
    
     return jsonify({"status":True})



    except Exception as e:
        print("eeeeeeeeeeeeeee")
        print(e)


@app.route('/get_image', methods=['GET'])
def get_image():
    # data = request.get_json()
    bucket_name = "designfinder"  # Update with your bucket name
    filename = request.args.get('filename')
    print(filename)

    # Fetch the image data from S3
    try:
        print()
        response = s3_service.read_file_from_s3_local(Bucket=bucket_name, Key=str(filename))
        image_data = response['Body'].read()

        # Set the appropriate content type for the image
        content_type = response['ContentType']

        # Return the image data with the appropriate content type
        return send_file(
            io.BytesIO(image_data),
            mimetype=content_type
        )
    except Exception as e:
        # Handle exceptions such as file not found
        print (str(e))
        return str(e), 404



@app.route('/add_carpet', methods=['POST'])
def add_carpet():
        data = request.get_json()
        array = data["files"]
        user = database["users"].find_one({"_id": ObjectId(data["user_id"])})
        print(user)
        st1 = Search_Setup(image_list=image_list, file_path='vgg19', pretrained=True, image_count=107)
        user_id = user["_id"]
        for each in array:
            print(each)
            database["collections"].find_one_and_update({"_id": ObjectId(data["collection_id"])},{"$push":{"images":each}})
            file = s3_service.read_file_from_s3(f"jay/collectio1/{each}",local_path=each)
            # print(file)

           
        file = st1.add_images_to_index(array,user_id)
        s3_service.upload_file(file_path=f'test/{user_id}.pkl',bucket_name="designfinder",object_key=f"jay/meta/image_data_features1.pkl")
        s3_service.upload_file(file_path=f'test/{user_id}.idx',bucket_name="designfinder",object_key=f"jay/meta/image_features_vectors2.idx")
        remove_files(f"test/{user_id}.pkl")
        remove_files(f"test/{user_id}.idx")
        for each in array:
            remove_files(f"test/{each}")
        return jsonify({"status":True})


@app.route('/carpets')
def carpets():
    headers = {'Content-Type': 'application/json'}

    print('called')
    all_documents = "tako"
    all_documents = list(collection.find({}).sort("createdAt", -1))
    print(all_documents)


    if len(all_documents) > 0 : 
        for document in all_documents:
            document["_id"] = str(document["_id"])

    return jsonify({"carpets":all_documents})


@app.route('/main_carpet/<path:filename>')
def serve_image(filename):
    print('runiiiiiiiiiiiiiii')
    return send_from_directory('./main_carpet', filename)


@app.route('/test', methods=['POST'])
def test():


    data=request.get_json()
    st = Search_Setup(image_list=image_list, file_path='vgg19', pretrained=True, image_count=107)
    user_detail = database['users'].aggregate([{   "$match": { "email":data["email"] }     }  ])
    collection_name = data["collection_name"]
    email = user_detail['email']
    file_path = f"{email}/{collection_name}"
    folder_path = './uploads/'  # Destination folder
    if request.method == 'POST':   
        f = request.files['file'] 
        file_path = os.path.join(folder_path, f.name)
        f.save(file_path)   
        # return render_template("Acknowledgement.html", name = f.filename)   

    message = 'You have just run a Python script on the button press!'
    names = st.get_similar_images(image_path=file_path, number_of_images=10)
    print(names)
    names_str = {str(key): value for key, value in names.items()}

    print(names_str)

    # st.plot_similar_images(image_path = image_list[90],number_of_images=16)

    return jsonify(names_str)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8000)


  
