from flask import Flask, jsonify, redirect, render_template, request, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import basededonne as db


app = Flask(__name__)
app.secret_key = "change_this_to_a_random_secure_string_in_production"


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


def format_questions(id_quiz: int, titre_quiz: str, questions: list) -> dict:
    quiz_data = {
        "id": id_quiz,
        "title": titre_quiz,
        "questions": []
    }

    for id_question, question_text, reponses in questions:
        question_dict = {
            "id": id_question,
            "title": question_text,
            "answers": []
        }

        for id_rep, texte_rep, correct in reponses:
            question_dict["answers"].append({
                "id": id_rep,
                "title": texte_rep,
                "correct": correct
            })

        quiz_data["questions"].append(question_dict)

    return quiz_data


"""
tests

avec 1 question 1 bonne rep format_quiz(1,"quizzz", [(1,"comment tu t' appelle ?", [ (1,"edward", False), (2,"Robert", True), (3,"ezekielle", False) , (2,"sss", False) ])])

 avec 2 questions ft=format_questions(1,"quizzz", [
    (1,"comment tu t' appelle", [ (1,"edward", False), (2,"Robert", True), (3,"ezekielle", False) , (4,"sssssss", False)]),
    
    (2,"1+1 ? ", [ (5,"5", False), (6,"2", True), (7,"977", False) , (8,"67", False)])
    
    ]
            )
            
"""

@app.route("/api/get_quiz/<int:id_quiz>")
def quiz_api(id_quiz):
    #prend tous les quiz et cherche leur titres
    all_quizzes = db.get_all_quiz()
    titre_quiz = next((titre for q_id, titre in all_quizzes if q_id == id_quiz), None)

    # Si le quiz existe pas erreur
    if titre_quiz is None:
        return jsonify({"error": "Quiz introuvable"}), 404

    # prend les quiestions
    questions = db.get_qa_from(id_quiz)

    # Format pour json pour le js
    data = format_questions(id_quiz, titre_quiz, questions)
    return jsonify(data)

    


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



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        return "Non !!!.", 401

    user_record = db.get_user_by_username(username)
    if not user_record:
        return "invalide !!.", 401

    username_db, stored_hash, is_admin = user_record

    if not check_password_hash(stored_hash, password):
        return "NON !!!!", 401

   
    session["username"] = username_db
    session["is_admin"] = bool(is_admin)

    return redirect(url_for("index"))




if __name__ == "__main__":
    app.run(port=5555, debug=False)


