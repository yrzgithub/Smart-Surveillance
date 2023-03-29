import cv2
from mediapipe.python.solutions import drawing_utils,face_detection

detector = face_detection.FaceDetection(min_detection_confidence=.5,model_selection=1)  #model selection = 1 ; to detect larget faces (<5m); selection = 0 (<2m)

img = cv2.imread("suriya.jpg")
img.flags.writeable = False
results = detector.process(image=img)
img.flags.writeable = True
detections = results.detections
if not detections:
    print("Face Not detected")
else:
    for det in detections:
        width,height,shape = img.shape
        #cv2.putText(img,str(det.score),(width//2,height//2),cv2.FONT_HERSHEY_DUPLEX,.6,(255,255,255),2)
        drawing_utils.draw_detection(img,det,bbox_drawing_spec=drawing_utils.DrawingSpec(color=(255,255,255)))
        print("Face detected")
        cv2.imshow("Frame",0)
        cv2.imwrite("suryaop.jpg",img)