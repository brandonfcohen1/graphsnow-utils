from flask import Flask

#Create app and set configs
app = Flask(__name__)

@app.route("/")
def index():
    return("hello world")