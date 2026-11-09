import json

from flask import Flask, jsonify, redirect, render_template, request, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import basededonne as db


app = Flask(__name__)
app.secret_key = "xJ7$P9vLm2!Qk8#Rz5@Tn1&Ws4*Hb6YfC3dE9uNp0"


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

# Crée les utilisateurs par défaut avec un mot de passe haché s'ils n'existent pas
if not db.get_user_by_username("Robert"):
    db.create_user("Robert", generate_password_hash("oUsItItI"), True)
if not db.get_user_by_username("Alban"):
    db.create_user("Alban", generate_password_hash("244466666"), False)
if not db.get_user_by_username("Frederic EricFred"):
    db.create_user("Frederic EricFred", generate_password_hash("baheoyghluqvsjdfkbnphate^r£ZQFJ"), True)
    
    
    
@app.route("/")
def index():
    quiz_liste = db.get_all_quiz()
    # La page principale
    return render_template("index.html", quizzes=quiz_liste)


@app.route("/quiz")
def quiz():
    print("QUIZ PAGE")
    #La page ou le quiz se passerai
    return render_template("quiz.html")

def compute_score(quiz_id : int, answers : list[int]) -> tuple[int, int]:
    q_and_a = db.get_qa_from(quiz_id)
    total = len(q_and_a)
    correct = 0
    for question in q_and_a:
        for answer in question[2]:
            if answer[2] and answer[0] in answers:
                correct += 1
                break
    return correct, total

@app.route("/result")
def result():
    quiz_id = eval(request.args.get("quiz_id"))
    quiz_result = eval(request.args["quiz_result"])

    all_quizzes = db.get_all_quiz()
    titre_quiz = next((titre for q_id, titre in all_quizzes if q_id == quiz_id), None)

    correct, total = compute_score(quiz_id, quiz_result)
    print(correct, total)
    return render_template("result.html", correct=correct, total=total, title=titre_quiz)


def format_questions(id_quiz: int, titre_quiz: str, questions: list) -> dict:
    """
Fonction qui fera le format qui quiz pour l envoyer au js
"""
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
        return "Username et mot de passe ne peuvent pas être vides !", 400

    if len(username) > 50:
        return "Username trop long.", 400

    mdp_hashed = generate_password_hash(password)
    success = db.create_user(username, mdp_hashed)
    if not success:
        return "Ce nom d'utilisateur existe déjà.", 409

    # log in direct aores creation de compte
    session["username"] = username
    session["isAdmin"] = False

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
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
    session["isAdmin"] = bool(is_admin)

    return redirect(url_for("index"))

@app.route("/creer_quiz", methods=["GET", "POST"])
def create_quiz():
    if not session.get("username"):
        return redirect(url_for("login"))
    if not session.get("isAdmin"):
        return "Vous n'avez pas le droit : réservé aux administrateurs !", 403
    
    if request.method == "GET":
        return render_template("new_quiz.html")
    
    donnees = request.get_json() or {}
    titre_quiz = donnees.get("title", "").strip()
    questions_liste = donnees.get("questions", [])  

    if not titre_quiz or not questions_liste:
        return jsonify({"error": "Le titre et les questions sont obligatoires."}), 400

    quiz_data_bdd = []
    for q in questions_liste:
        question_text = q.get("title", "").strip()
        reponses = [
            (ans.get("title", "").strip(), bool(ans.get("correct", False)))
            for ans in q.get("answers", [])
            if ans.get("title", "").strip()
        ]
        # Vérifie que la question a un titre, au moins 2 réponses, et au moins 1 bonne réponse
        has_correct = any(correct for _, correct in reponses)
        if question_text and len(reponses) >= 2 and has_correct:
            quiz_data_bdd.append((question_text, reponses))
        else:
            return jsonify({
                "error": "Chaque question doit avoir un titre, au moins 2 réponses et au moins 1 réponse correcte."
            }), 400

    db.create_quizz(quiz_data_bdd, titre_quiz)
    return jsonify({"status": "success", "redirect": url_for("index")})
    


if __name__ == "__main__":
    app.run(port=5555, debug=False)


