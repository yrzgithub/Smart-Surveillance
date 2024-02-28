from os import remove,listdir,rename
from easygui import diropenbox
from os.path import abspath,join,splitext

folder = abspath(diropenbox(msg="Select images folder", title="Smart Surveillance"))
print(folder)

folders = listdir(folder)

old_img_folder = join(folder,folders[0])
old_labels_folder = join(folder,folders[1])

images_folder = join(folder,"images")
labels_folder = join(folder,"labels")

rename(old_img_folder,images_folder)
rename(old_labels_folder,labels_folder)

images = [splitext(path) for path in listdir(images_folder)]
labels = [splitext(path)[0] for path in listdir(labels_folder)]

print("labels length : ",len(labels))

for img,extension in images:
    if img not in labels:
        path = join(images_folder,img + extension)
        remove(path)
        print(path)