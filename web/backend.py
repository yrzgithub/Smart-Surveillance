from flask import *
from pyrebase import *
from face_recognition import *
from cvlib.object_detection import *
from os.path import *
from os import makedirs
from classes import *
import cv2 
from json import dumps
import numpy as np
from base64 import b64encode
import pickle



firebaseConfig = {
  "apiKey": "AIzaSyDKzdFq44XLPspZEsfLBWtfmzQYp9KB0jk",
  "authDomain": "smart-surveillance-37cd5.firebaseapp.com",
  "databaseURL": "https://smart-surveillance-37cd5-default-rtdb.firebaseio.com",
  "projectId": "smart-surveillance-37cd5",
  "storageBucket": "smart-surveillance-37cd5.appspot.com",
  "messagingSenderId": "53238167841",
  "appId": "1:53238167841:web:ddb1fe20aeb4bba08d2660"
}



conf = "models\yolo-tiny-obj.cfg"
weights = "models\yolo-tiny-obj.weights"
labels = "models\obj.names"
dataPathFace = abspath("data\dataFace.pkl")
pathFaces = abspath("data\\faces")



data = []

if not isdir("data"):
    makedirs("data")

if not isdir(pathFaces):
    makedirs(pathFaces)


if isfile(dataPathFace):
    with open(dataPathFace,"rb") as file:
        fd = pickle.load(file)
        data.extend(fd)
        file.close()



yolo = YOLO(config=conf,weights=weights,labels=labels,version="yolo-tiny")



app = Flask(__name__)

firebase = initialize_app(firebaseConfig)
auth = firebase.auth()



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/detect",methods=["POST"])
def detect():
    form = request.form 
    username = form["username"].strip()
    password = form["password"].strip()

    result = None

    try:
        result = auth.sign_in_with_email_and_password(username,password)
        return render_template("detect.html")

    except Exception as e:
        return render_template("error.html",error = e)


@app.route("/object/{weapon}")
def obj(weapon):
    return render_template("obj.html")


@app.route("/face/{face}")
def face(face):
    return render_template("face.html")


@app.route("/addFace")
def addImg():
    return render_template("addFace.html")


def getEncodedImage(type_,img):
    image = f"data:{type_};base64," + b64encode(cv2.imencode(".jpeg",img)[1]).decode()
    return image


@app.route("/uploadFace",methods=["POST"])
def uploadFace():
    img = request.files["file"]
    type_ = img.content_type.replace("image/","") 
    print(type_)

    print("Decoding...")

    image = cv2.imdecode(np.frombuffer(bytearray(img.read()),np.uint8),cv2.IMREAD_COLOR)

    print("Encoding Face..")

    face_encoding = face_encodings(image)

    len_face_encodings = len(face_encoding)
    
    if len_face_encodings == 0:
        return dumps({"error":"No Face Found."})
    
    print("Locating Face...")
    
    a,b,c,d = face_locations(image)[0]
    image = cv2.rectangle(image,(d,a),(b,c),(51,255,255),3)
    success,buffer = cv2.imencode(".png",image)
    
    if len_face_encodings > 1:
        return dumps({"error":"More than one face found.","img":getEncodedImage(img.content_type,image)})

    args = request.form

    name = args["name"]
    age = args["number"]
    religion = args["religion"]
    illness = args["illness"]
    position = args["position"]
    group = args["group"]
    residence = args["residence"]

    terrorist = Terrorist(name)
    terrorist.setAge(age)
    terrorist.setReligion(religion)
    terrorist.setIllness(illness)
    terrorist.setPosition(position)
    terrorist.setGroup(group)
    terrorist.setCountry(residence)
    terrorist.setId(len(data))

    data.append(terrorist)

    with open(dataPathFace,"wb") as file:
        pickle.dump(data,file)
        file.close()

    return dumps({"msg":"Image Uploaded","img":getEncodedImage(img.content_type,image)})



app.run(debug=True)