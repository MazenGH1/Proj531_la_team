from flask import Flask, render_template
from basededonne import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quiz")
def quiz():
    pass
    #return render_template("quiz.html")

app.run()