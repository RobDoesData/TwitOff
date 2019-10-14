#import flask package. flask makes app objects.
from flask import Flask, render_template

#create Flask web server, makes the application
app = Flask(__name__)

#routes determine location
@app.route("/")

#Define simple function
def home():
    return render_template('home.html')

@app.route("/about")
def preds():
    return render_template('about.html')
