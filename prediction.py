from tensorflow import keras
import cv2
import numpy as np

model = keras.models.load_model("model/CPN_Model.h5")
resize = 150

def preprocess_image(image):
    image = cv2.imread(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    image = cv2.resize(image, (resize, resize)) /255
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    return image

def prediction(image):
    image = preprocess_image(image)
    output = model.predict(image)
    output = np.argmax(output,axis=1)
    if output == 0:
        return 'COVID-19'
    elif output == 1:
        return 'Normal'
    else:
        return 'Pneumonia'
 32  
server.py
@@ -0,0 +1,32 @@
from flask import Flask, render_template, redirect, request, url_for, send_file
from flask import jsonify, json
from werkzeug.utils import secure_filename
import prediction
import os


app = Flask("__main__", template_folder="templates")
Uploaded_images = "Uploaded_images"
app.config['Uploaded_images'] = Uploaded_images

@app.route('/', methods=['POST', 'GET'])
def homepage():
  if request.method == 'GET':
    return render_template('index.html')

@app.route('/getFile', methods=['POST'])
def getOutput():
  output=""
  if request.method == 'POST':
        myimage = request.files.get('myfile')
        imgname = secure_filename(myimage.filename)
        imgpath = "Uploaded_images/"+imgname
        myimage.save(os.path.join(app.config["Uploaded_images"], imgname))
        output = prediction.prediction(imgpath)
        print(output)
        return output




app.run(port=3000);