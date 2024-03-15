from os.path import isfile,isdir,abspath
from os import makedirs
import pickle



class Terrorist:

    name = ""
    img = None
    age = 20
    country = ""
    group = ""
    religion = ""
    position = ""
    id = 0
    illness = ""
    face_encoding = None


    def __init__(self,name):
        self.name = name
    

    def getName(self):
        return self.name 
    

    def getId(self):
        return id
    

    def getImg(self):
        return self.img 
    

    def getAge(self):
        return self.age 
    

    def getCountry(self):
        return self.country 
    

    def getGroup(self):
        return self.group
    

    def getReligion(self):
        return self.religion 
    

    def getPosition(self):
        return self.position 
    

    def getIllness(self):
        return self.illness
    

    def getFaceEncodings(self):
        return self.face_encoding
    

    def setName(self,name):
        self.name = name 
    

    def setImg(self,img):
        self.img = img


    def setId(self,id):
        self.id = id
    

    def setAge(self,age):
        self.age = age 
        

    def setCountry(self,country):
        self.country = country
    

    def setGroup(self,group):
        self.group = group 
    

    def setReligion(self,religion):
        self.religion = religion
    

    def setPosition(self,position):
        self.position = position
    

    def setIllness(self,illness):
        self.illness = illness
    

    def saveFaceEncodings(self,encodings):
        self.face_encoding = encodings



class Weapon:

    name = ""
    color = ""
    type = ""
    power = ""
    image = ""
    accuracy = ""
    range = ""
    portability = ""


    def __init__(self,name):
        self.name = name


    def getName(self):
        return self.name 
    

    def getColor(self):
        return self.color 
    

    def getType(self):
        return self.type 

    
    def getPower(self):
        return self.power 
    

    def getAccuracy(self):
        return self.accuracy
    

    def getRange(self):
        return self.range 
    

    def getPortability(self):
        return self.portability
    

    def getImage(self):
        return self.image
    

    def setImage(self,image):
        self.image = image
    

    def setName(self,name):
        self.name = name
    

    def setColor(self,color):
        self.color = color 
    

    def setType(self,type):
        self.type = type

    
    def setPower(self,power):
        self.power = power
    

    def setAccuracy(self,accuracy):
        self.accuracy = accuracy
    

    def setRange(self,range):
        self.range = range
    

    def setPortability(self,portability):
        self.portability = portability