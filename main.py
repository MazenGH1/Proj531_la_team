from flask import Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import basededonne as db


app = Flask(__name__)


db.init_BDD()
existing_quizzes = db.get_all_quiz()
if len(existing_quizzes) == 0:
    print("Database empty! Inserting sample quiz...")
    db.create_quizz(
        [
            ("Quelle est la capitale de la Suisse ?",
             [("Berne", True), ("Genève", False), ("Bâle", False)]),
            ("Combien font 7+7 ?",
             [("13", False), ("14", True), ("15", False)]),
        ],
        "Quiz 1"
    )
    
    
    
@app.route("/")
def index():
    quiz_liste = db.get_all_quiz()
    return render_template("index.html", quizzes=quiz_liste)


@app.route("/quiz")
def quiz():
    print("QUIZ PAGE")
    return render_template("quiz.html")

@app.route("/result")
def result():
    return render_template("result.html")

def format_questions(questions):
    res = {}
    for id_question, question, reponses in questions:
        res[question] = {rep: bool(correct) for _, rep, correct in reponses}
    return res

#test format_questions([(1,"comment tu t' appelle", [ (1,"edward", False), (2,"Robert", True), (3,"ezekielle", False) , (2,"sss", False) ])])


@app.route("/api/get_quiz/<int:id_quiz>")
def quiz_api(id_quiz):
    print("API REQUEST", id_quiz)
    questions = db.get_qa_from(id_quiz)
    print("AFTER DB")
    return jsonify(format_questions(questions))


    


@app.route("/cree", methods=["GET", "POST"])
def cree_compte():
    if request.method == "GET":
        return render_template("cree.html")
    
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        return "Username et mot de passe ne peuvent pas etre vide !!!!!", 400

    if len(username) > 50:
        return "username trop long.", 400

    mdp_hashed = generate_password_hash(password)
    success = db.create_user(username, mdp_hashed)
    if not success:
        return "Username existe deja.", 409

    return redirect(url_for("index"))



@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        return "Non !!!.", 401

    # Fetch les information safely de la BDD
    user_record = db.get_user_by_username(username)
    if not user_record:
        return "invalide !!.", 401

    _, stored_hash, is_admin = user_record

    # Verify password against hash
    if not check_password_hash(stored_hash, password):
        return "NON !!!!", 401

    return redirect(url_for("index"))




if __name__ == "__main__":
    app.run(port=5555, debug=False)


