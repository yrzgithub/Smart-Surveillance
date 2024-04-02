import cv2
from keyboard import is_pressed
from face_recognition import face_encodings,compare_faces,face_locations
from os import listdir
from easygui import fileopenbox
from os.path import *
from pafy import new
from pickle import load,dump
from youtubesearchpython import VideosSearch
from cvlib.object_detection import YOLO
from pyrebase import initialize_app
import numpy
from requests import get



faces_path = r"faces"
ser_path = r"data/data.pkl"
weights = "models\yolo-tiny-obj.weights"
config = "models\yolo-tiny-obj.cfg"
labels = "models\obj.names"

test = abspath("test\images")

use_img = False
use_yt = False
stream = False
<<<<<<< HEAD
use_cloud = False
use_video = True
=======
use_cloud = True
use_video = False
>>>>>>> fe017176548a0cc14ebf3dcc3a93afa643698b56

known_face_names = ["Ram","Raj"]



if isfile(ser_path):
    print("Face encodings found...")
    with open(ser_path,"rb") as file:
        face_encodings_data = load(file)
        file.close()

else:
    print("Reading face encodings")

    face_encodings_data = []
    for face in listdir(faces_path):
        print(f"Reading file : {face}")
        face_encodings_data.append(face_encodings(cv2.imread(join(faces_path,face)))[0])
    
    print("Saving encoding data..")
    
    with open(ser_path,"wb") as file:
        dump(face_encodings_data,file)
        file.close()

    print("encoding data saved..")



model = YOLO(weights=weights,config=config,labels=labels,version="yolo-tiny")
img_index = 0

firebaseConfig = {
  "apiKey": "AIzaSyDKzdFq44XLPspZEsfLBWtfmzQYp9KB0jk",
  "authDomain": "smart-surveillance-37cd5.firebaseapp.com",
  "databaseURL": "https://smart-surveillance-37cd5-default-rtdb.firebaseio.com",
  "projectId": "smart-surveillance-37cd5",
  "storageBucket": "smart-surveillance-37cd5.appspot.com",
  "messagingSenderId": "53238167841",
  "appId": "1:53238167841:web:ddb1fe20aeb4bba08d2660"
}

app = initialize_app(config=firebaseConfig)

storage = app.storage()
auth = app.auth()

user = auth.sign_in_with_email_and_password("seenusanjay20102002@gmail.com","#Jaihind20")


if not use_cloud:
    source = input("Paste the source : ")


if use_img:
    source = listdir(test)
    source_len = len(source)

elif use_video:
        filename = fileopenbox(msg="Select video file",title="Smart Surveillance",filetypes="videos/*")
        source = cv2.VideoCapture(filename)
    
elif use_yt:
    stream_url = new(input("paste yt link : ")).getbestvideo().url
    print(stream_url)
    source = cv2.VideoCapture(stream_url)

elif stream:
    source = cv2.VideoCapture(input("Stream link : "))

else:
    source = cv2.VideoCapture(0) 

source_len = 0


while source.isOpened() and not is_pressed("esc"):

    if use_img:

        if img_index < source_len:
            img = cv2.imread(join(test,source[img_index]))
        
        else:
            break

    elif use_cloud:
        link = storage.child("image.jpg").get_url(user["idToken"])
        arr = numpy.asarray(bytearray(get(link).content),numpy.uint8)
        img = cv2.imdecode(arr,cv2.IMREAD_COLOR)

    else:
        _,img = source.read()

    current_face_encodings = face_encodings(img)
    if len(current_face_encodings)==0:
        print("No face available")

    for face_data in current_face_encodings:
        try:
            comparison = compare_faces(face_encodings_data,face_data,tolerance=0.5)
            locations = face_locations(img)

            for (a,b,c,d) in locations:
                cv2.rectangle(img, (d, a), (b, c), color=(250, 0, 250), thickness=2) 

            print("Face detected",known_face_names[comparison.index(True)])

        except:
            print("Unknown face detected")
    
    bboxs,labels,confidences = model.detect_objects(img)
    model.draw_bbox(img,bboxs,labels,confidences)

    for index,label in enumerate(labels):
        bbox = bboxs[index]
        confidence = confidences[index]

        print(label,confidence)
    
    # img = cv2.resize(img,(1000,500))

    cv2.imshow("Frame",cv2.resize(img,(500,500)))
    cv2.waitKey(1)

    img_index += 1



if isinstance(source,cv2.VideoCapture):
    source.release()


cv2.destroyAllWindows()