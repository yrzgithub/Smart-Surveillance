from requests import get
from easygui import diropenbox
from os.path import join
from os import listdir

name = input("Enter the query : ")
count = int(input("no. of images : ")) + 1 

folder = diropenbox("Select test folder",title="surveillance")

start = len(listdir(folder))
count = start + count

url = "https://source.unsplash.com/random?" + name 

for i in range(start,count):
    with open(join(folder,str(i)+".png"),"wb") as file:
        print(i)
        file.write(get(url).content)
        file.close()