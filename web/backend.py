from flask import *
from pyrebase import *
from face_recognition import *
from cvlib.object_detection import *
from os.path import *
from os import makedirs
from classes import *
import cv2 
from requests import get
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


imgUrl = "https://firebasestorage.googleapis.com/v0/b/smart-surveillance-37cd5.appspot.com/o/image.jpg?alt=media&token=74ea648b-3d1c-4a3b-aeec-6ba192ae4e3c"



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


known_face_encodings = [terrorist.getFaceEncodings() for terrorist in data]



yolo = YOLO(config=conf,weights=weights,labels=labels,version="yolo-tiny")



app = Flask(__name__)

firebase = initialize_app(firebaseConfig)
auth = firebase.auth()



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/detect",methods=["POST"])
def detect():
    site = {}

    form = request.form 
    username = form["username"].strip()
    password = form["password"].strip()

    result = None

    image = cv2.imdecode(np.frombuffer(bytearray(get(imgUrl).content)),cv2.IMREAD_COLOR)

    face_encodings = face_encodings(image)

    locations = face_locations(image)

    for location in locations:
        a,b,c,d = location 
        image = cv2.rectangle(image,(d,a),(b,c),(51,225,225),3)

    bboxs,labels,confs = yolo.detect_objects(image)
    image = draw_bbox(image,bboxs,labels,confs,(193,182,225),True)

    site["objects"] = labels
    site["faces"] = []

    for encodings in face_encodings:
        faceList = face_distance(known_face_encodings,encodings)
        maximum = max(faceList)
        if maximum < 0.6:
            break 
        index = faceList.index(maximum)
        location = locations[index]
        detected_terrorist = data[index]
        site["faces"].append(detected_terrorist.getName())
        (a,b,c,d) = location
        image = cv2.putText(image,detected_terrorist.getName(),(a,c),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2,cv2.LINE_AA)

    try:
        result = auth.sign_in_with_email_and_password(username,password)
        return render_template("detect.html",site = site)

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
    image = f"data:{type_};base64," + b64encode(cv2.imencode(type_,img)[1]).decode()
    return image


@app.route("/uploadFace",methods=["POST"])
def uploadFace():
    img = request.files["file"]

    print("Decoding...")

    image = cv2.imdecode(np.frombuffer(bytearray(img.read()),np.uint8),cv2.IMREAD_COLOR)

    print("Encoding Face..")

    face_encoding = face_encodings(image)

    len_face_encodings = len(face_encoding)
    
    if len_face_encodings == 0:
        return dumps({"error":"No Face Found."})
    
    print("Locating Face...")
    
    for location in face_locations(image):
        a,b,c,d = location(image)
        image = cv2.rectangle(image,(d,a),(b,c),(51,255,255),3)
    
    if len_face_encodings > 1:
        return dumps({"error":"More than one face found.","img":getEncodedImage(".png",image)})

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
    
    print("Writing Image...")
    cv2.imwrite(f"data\\faces\\{terrorist.id}.png",image)

    return dumps({"msg":"Image Uploaded","img":getEncodedImage(".png",image)})



app.run(debug=True)