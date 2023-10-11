import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from DeepImageSearch import Load_Data,Search_Setup
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from fileinput import filename 

image_list = Load_Data().from_folder(['./main carpet'])
st = Search_Setup(image_list=image_list, model_name='vgg19', pretrained=True, image_count=100)
st.run_index()

app = Flask(__name__)
CORS(app)


# Using the below, the popup message appears when the button is clicked on the webpage.
@app.route('/test', methods=['POST'])
def test():

    if request.method == 'POST':   
        f = request.files['file'] 
        folder_path = './uploads/'  # Destination folder
        file_path = os.path.join(folder_path, f.filename)
        # f.save(file_path)   
        # return render_template("Acknowledgement.html", name = f.filename)   

    message = 'You have just run a Python script on the button press!'
    names = st.get_similar_images(image_path=f, number_of_images=10)
    names_str = {str(key): value for key, value in names.items()}

    # st.plot_similar_images(image_path = image_list[90],number_of_images=16)

    
   
    
    return jsonify(names_str)

if __name__ == "__main__":
    app.run(debug=True)


  
