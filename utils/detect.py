from cvlib.object_detection import YOLO
from os.path import *
from os import *
import cv2
import numpy
from requests import get
from keyboard import is_pressed



weights = "models\yolo-tiny-obj.weights"
config = "models\yolo-tiny-obj.cfg"
labels = "models\obj.names"


test = abspath("D:\My Apps\ObjectDetectionCode\images\military aircraft")
download = abspath("test\images\download")


use_web = 1


model = YOLO(weights=weights,config=config,labels=labels,version="yolo-tiny")


def rectangle(img):
    bboxs,labels,confidences = model.detect_objects(img,confidence=0.7)

    for index,box in enumerate(bboxs):
        a,b,c,d = box
        img = cv2.rectangle(img,(a,b),(c,d),(51,225,225),2)
        img = cv2.putText(img,labels[index],(c-50,d+30),fontScale=2,fontFace=cv2.FONT_HERSHEY_PLAIN,color=(0,0,225),thickness=2,lineType=cv2.LINE_AA)

    return img,bboxs,labels,confidences


if use_web:
    name = input("Enter the query : ")
    url = "https://source.unsplash.com/random?" + name 

    index = 0
    while True:
        index += 1
        image = cv2.imdecode(numpy.frombuffer(bytearray(get(url).content),numpy.uint8),cv2.IMREAD_COLOR)
        image,bboxs,labels,confidences = rectangle(image)
        # print(cv2.imwrite(f"{download}\\{index}.png",image))
        cv2.imshow("Frame",image)
        cv2.waitKey(100)

        if is_pressed("esc"):
            cv2.destroyAllWindows()
            exit(0)


files = listdir(test)
print(len(files),"images found")


n = 0
for file in files:

    if is_pressed("esc"):
        break

    img = cv2.imread(join(test,file))

    if type(img) == None:
        continue

    img,bboxs,labels,confidences = rectangle(img)

    if len(labels) == 0:
        continue

    for index,label in enumerate(labels):
        bbox = bboxs[index]
        confidence = confidences[index]

        print(label,confidence)

    print(cv2.imwrite(f"{download}\\{n}.png",img))

    cv2.imshow("Frame",img)
 
    cv2.waitKey(1)
    n += 1