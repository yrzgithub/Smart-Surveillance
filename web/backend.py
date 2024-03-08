from flask import *



class Terrorist:

    name = ""
    img = None
    age = 20
    country = ""
    group = ""
    religion = ""
    position = ""
    illness = ""

    def __init__(self,name,img):
        self.name = name
        self.img = img 
    

    def getName(self):
        return self.name 
    

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
    

    def setName(self,name):
        self.name = name 
    

    def setImg(self,img):
        self.img = img
    

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



class Weapon:

    name = ""
    img = None
    color = ""
    type = ""
    power = ""
    accuracy = ""
    range = ""
    reliability = ""
    portability = ""


    def __init__(self,name,img):
        self.name = name
        self.img = img


    def getName(self):
        return self.name 
    

    def getImg(self):
        return self.img 
    

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
    

    def getReliability(self):
        return self.reliability 
    

    def getPortability(self):
        return self.portability
    

    def setName(self,name):
        self.name = name
    

    def setImg(self,img):
        self.img = img
    

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
    

    def setReliability(self,reliability):
        self.reliability = reliability
    

    def setPortability(self,portability):
        self.portability = portability
        


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/detect",methods=["POST"])
def detect():
    form = request.form 
    username = form["username"].strip()
    password = form["password"].strip()
    print(username,password)
    return render_template("detect.html")


@app.route("/object/{weapon}")
def obj(weapon):
    return render_template("obj.html")


@app.route("/face/{face}")
def obj(face):
    return render_template("face.html")


app.run(debug=True)