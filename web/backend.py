from flask import *
from pyrebase import *
from face_recognition import *
from cvlib.object_detection import *
from os.path import *
from os import makedirs
from classes import *



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


@app.route("/uploadFace",methods=["POST"])
def uploadFace():
    img = request.files["file"]

    args = request.form
    print(args)

    name = args["name"]
    age = args["number"]
    religion = args["religion"]
    illness = args["illness"]
    position = args["position"]
    group = args["group"]
    residence = args["residence"]

    terrorist = Terrorist(name,img)
    terrorist.setAge(age)
    terrorist.setReligion(religion)
    terrorist.setIllness(illness)
    terrorist.setPosition(position)
    terrorist.setGroup(group)
    terrorist.setCountry(residence)

    terrorist.saveFace()

    return Response(status=200)



app.run(debug=True)