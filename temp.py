import cv2
from keyboard import is_pressed
from mediapipe.python.solutions import drawing_utils,face_detection
from face_recognition import face_encodings,compare_faces,face_locations
from os import listdir
from os.path import isfile,join
from pickle import load,dump


detect_only = False

faces_path = r"D:\Live In Lab (Smart Surveillance)\Code\faces"
ser_path = r"D:\Live In Lab (Smart Surveillance)\Code\data.pkl"

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
detector = face_detection.FaceDetection(min_detection_confidence=.5,model_selection=1)  #model selection = 1 ; to detect larget faces (<5m); selection = 0 (<2m)

while not is_pressed("esc"):
    _,img = camera.read()
    if detect_only:
        img.flags.writeable = False
        results = detector.process(image=img)
        img.flags.writeable = True
        detections = results.detections
        if not detections:
            print("Face Not detected")
        else:
            for det in detections:
                width,height,shape = img.shape
                cv2.putText(img,str(det.score),(width//2,height//2),cv2.FONT_HERSHEY_DUPLEX,.6,(255,255,255),2)
                drawing_utils.draw_detection(img,det,bbox_drawing_spec=drawing_utils.DrawingSpec(color=(255,255,255)))
                print("Face detected")

    else:
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