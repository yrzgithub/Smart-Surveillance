from cvlib.object_detection import YOLO
from os.path import *
from os import *
import cv2


weights = "models\yolo-tiny-obj.weights"
config = "models\yolo-tiny-obj.cfg"
labels = "models\obj.names"

test = abspath("test\images")


model = YOLO(weights=weights,config=config,labels=labels,version="yolo-tiny")


files = listdir(test)
print(len(files),"images found")


for file in files:
    img = cv2.imread(join(test,file))

    bboxs,labels,confidences = model.detect_objects(img)
    model.draw_bbox(img,bboxs,labels,confidences)

    for index,label in enumerate(labels):
        bbox = bboxs[index]
        confidence = confidences[index]

        print(label,confidence)

    cv2.imshow("Frame",img)
    cv2.waitKey(100)
