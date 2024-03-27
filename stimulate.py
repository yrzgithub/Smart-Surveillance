from pyrebase import initialize_app
import os
from time import sleep



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


username = "seenusanjay20102002@gmail.com"
password = "#Jaihind20"


user = auth.sign_in_with_email_and_password(username,password)
idToken = user["idToken"]


if not os.path.isdir("live"):
    exit("Live Dir not found...")


files = os.listdir("live")
for file in files:
    path = f"live\\{file}"

    with open(path,"rb") as file:
        print("Uploading ",path)
        storage.child("image").put(file,token=idToken,content_type="image\jpg")
        print("uploaded...")
        file.close()

    sleep(3)