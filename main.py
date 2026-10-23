from flask import Flask, render_template
from basededonne import *

app = Flask(__name__)

@app.route("/")
def index():
    quiz_liste= get_all_quiz()
    return render_template("index.html", quizzes=quiz_liste)


@app.route("/quiz")
def quiz():
    pass
    #return render_template("quiz.html")

@app.route("/result")
def result():
    pass
    #return render_template("result.html")

@app.route("/Api/get_quiz", methods=["GET"])
def quiz_api():
    pass

app.run()