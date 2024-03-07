from flask import *


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


app.run(debug=True)