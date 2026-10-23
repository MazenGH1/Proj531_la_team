from flask import Flask, render_template, jsonify
import basededonne as db

app = Flask(__name__)

@app.route("/")
def index():
    #quiz_liste = db.get_all_quiz()
    return render_template("index.html")

"""

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/api/get_quiz/<int:id_quiz>", methods=["GET"])
def quiz_api(id_quiz):
    quiz = db.get_quiz(id_quiz)
    return jsonify(format_questions(quiz))


def format_questions(questions):
    res = {}
    for _ , question, reponses in questions:
        res[question] = {rep: correct for _, rep, correct in reponses}
    return res

#test format_questions([(1,"comment tu t' appelle", [ (1,"edward", False), (2,"Robert", True), (3,"ezekielle", False) , (2,"sss", False) ])])




app.run()
"""