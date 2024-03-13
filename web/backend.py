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
prev = None



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

    global prev 

    prev = None

    form = request.form 
    username = form["username"].strip()
    password = form["password"].strip()

    result = None

    try:
        result = auth.sign_in_with_email_and_password(username,password)
        return render_template("detect.html")

    except Exception as e:
        return render_template("error.html",error = e)
    

@app.route("/getimage")
def getimage():
    global prev 

    site = {}

    print("Decoding...")

    content = get(imgUrl).content

    if prev == content:
        return dumps({"error":"alerady processed"})
    
    prev = content

    image = cv2.imdecode(np.frombuffer(bytearray(content),np.uint8),cv2.IMREAD_COLOR)

    print("Encoding faces...")

    fencodings = face_encodings(image)

    print("Locating Images...")

    locations = face_locations(image)

    for location in locations:
        a,b,c,d = location 
        image = cv2.rectangle(image,(d,a),(b,c),(51,225,225),1)
    
    print("Detecting Objects...")

    bboxs,labels,confs = yolo.detect_objects(image)
    image = draw_bbox(image,bboxs,labels,confs,(193,182,225),True)

    site["objects"] = labels
    site["faces"] = []

    print("Recognizing...")

    for encodings in fencodings:
        faceList = list(face_distance(known_face_encodings,encodings))
        print(faceList)
        minumum = min(faceList)
        if minumum >= 0.6:
            break 
        index = faceList.index(minumum)
        location = locations[index]
        detected_terrorist = data[index]
        site["faces"].append(detected_terrorist.getName())
        (a,b,c,d) = location
        image = cv2.putText(image,detected_terrorist.getName(),(a+12,c+12),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1,cv2.LINE_AA)

    return dumps({"img":getEncodedImage(".png",image),"faces":site["faces"],"objects":site["objects"]})


@app.route("/object/<weapon>")
def obj(weapon):
    name =  list(filter(lambda terror : terror.getName() == weapon,data))[0]
    return render_template("obj.html",weapon = name)


@app.route("/face/<face>")
def face(face):
    name =  list(filter(lambda terror : terror.getName() == face,data))[0]
    return render_template("face.html",terrorist = name)


@app.route("/addFace")
def addImg():
    return render_template("addFace.html")


def getEncodedImage(type_,img):
    image = f"data:{type_};base64," + b64encode(cv2.imencode(type_,img)[1]).decode()
    return image


@app.route("/uploadFace",methods=["POST"])
def uploadFace():
    global data 

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
        a,b,c,d = location
        image = cv2.rectangle(image,(d,a),(b,c),(51,255,255),1)
    
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

    encoded = getEncodedImage(".png",image)

    terrorist = Terrorist(name)
    terrorist.setAge(age)
    terrorist.setReligion(religion)
    terrorist.setIllness(illness)
    terrorist.setPosition(position)
    terrorist.setGroup(group)
    terrorist.setCountry(residence)
    terrorist.setId(len(data))
    terrorist.saveFaceEncodings(face_encoding[0])
    terrorist.setImg(encoded)

    data.append(terrorist)
    known_face_encodings.append(face_encoding[0])

    with open(dataPathFace,"wb") as file:
        pickle.dump(data,file)
        file.close()
    
    print("Writing Image...")
    cv2.imwrite(f"data\\faces\\{terrorist.id}.png",image)

    return dumps({"msg":"Image Uploaded","img":encoded})



app.run(debug=True)