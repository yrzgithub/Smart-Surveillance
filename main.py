import cv2
from keyboard import is_pressed
from face_recognition import face_encodings,compare_faces,face_locations
from os import listdir
from os.path import isfile,join
from pickle import load,dump

faces_path = r"faces"
ser_path = r"data/data.pkl"

known_face_names = ["Ram","Raj"]

if isfile(ser_path):
    face_encodings_data = load(ser_path)

else:
    print("Reading face encodings")
    face_encodings_data = []
    for face in listdir(faces_path):
        print(f"Reading file : {face}")
        face_encodings_data.append(face_encodings(cv2.imread(join(faces_path,face)))[0])

camera = cv2.VideoCapture(0)

while not is_pressed("esc"):
    _,img = camera.read()

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

    cv2.imshow("Frame",img)
    cv2.waitKey(1)

cv2.destroyAllWindows()