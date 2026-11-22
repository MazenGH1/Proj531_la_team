import json

from flask import Flask, jsonify, redirect, render_template, request, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import basededonne as db


app = Flask(__name__)
app.secret_key = "xJ7$P9vLm2!Qk8#Rz5@Tn1&Ws4*Hb6YfC3dE9uNp0"
ADMIN_SECRET_KEY = "kirk"


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
    
    db.create_quizz(
        [
            ("Qui est le GOAT du football",
             [("Cristiano Ronaldo", True), ("Lionel Messi", False), ("Alban Stora", False),("Maradona ", False)]),
            ("Quel club a le plus de Champions League",
             [("Real Madrid", True), ("PSG", False), ("Arsenal", False),("AC Milan", False)]),
            
            ("Combien de Champions League Real Madrid a",
             [("13", False), ("15", True), ("2", False),("5", False)]),
            
            
             ("Combien de Ballon d'or Neyman Jr a ",
             [("3", True), ("4", False), ("0", True),("1", False)])
        ],
        "Football"
    )
    
    db.create_quizz(
        [
            
            ("Dérivée de sin(x) ?",
             [("cos(x)", True), ("-cos(x)", False), ("-sin(x)", False), ("tan(x)", False)]),
            ("Dérivée de ln(x) ?",
             [("e^x", False), ("1/x", True), ("ln(x)/x", False), ("x", False)]),
            ("Dérivée de tan(x) ?",
             [("1/sin²(x)", False), ("-1/cos²(x)", False), ("1 + tan²(x)", True), ("cot(x)", False)]),
            ("Dérivée de arctan(x) ?",
             [("1/√(1 − x²)", False), ("1/(1 + x²)", True), ("−1/(1 + x²)", False), ("1/(1 − x²)", False)]),
            ("Dérivée de x^x (x > 0) ?",
             [("x · x^(x−1)", False), ("x^x · ln(x)", False), ("x^x", False), ("x^x (ln(x) + 1)", True)]),

            
            ("∫₀¹ x² dx = ?",
             [("1/2", False), ("2/3", False), ("1/3", True), ("1", False)]),
            ("∫₀^π sin(x) dx = ?",
             [("0", False), ("1", False), ("π", False), ("2", True)]),
            ("∫₀^∞ sin(x)/x dx = ?",
             [("π", False), ("π/2", True), ("1", False), ("2", False)]),
            ("∫₀^∞ e^(−x) dx = ?",
             [("0", False), ("e", False), ("1", True), ("+∞", False)]),

            
            ("∫ de −∞ à +∞ de e^(−x²) dx = ?",
             [("√π", True), ("π", False), ("2π", False), ("1", False)]),
            ("∫ de −∞ à +∞ de e^(−x²/2) dx = ?",
             [("√π", False), ("2π", False), ("√(2π)", True), ("1", False)]),
            ("Densité de la loi normale N(0,1) ?",
             [("e^(−x²) / √π", False), ("e^(−x²/2) / √(2π)", True), ("e^(−x²/2) / (2π)", False), ("e^(−x) / √(2π)", False)]),
            ("Γ(1/2) = ?",
             [("π", False), ("1", False), ("√(2π)", False), ("√π", True)]),

            
            ("Σ (n≥1) 1/n² = ?",
             [("π/4", False), ("π²/6", True), ("π²/3", False), ("ln 2", False)]),
            ("Σ (n≥0) 1/n! = ?",
             [("π", False), ("2", False), ("e", True), ("1/e", False)]),
            ("Σ (n≥0) x^n pour |x| < 1 ?",
             [("1/(1 + x)", False), ("x/(1 − x)", False), ("1/(1 − x)", True), ("e^x", False)]),
            ("Σ (n≥1) (−1)^(n+1)/n = ?",
             [("π/4", False), ("1", False), ("ln 2", True), ("π²/12", False)]),
            ("Σ (n≥0) (−1)^n/(2n+1) = ?",
             [("π/2", False), ("ln 2", False), ("π²/6", False), ("π/4", True)]),
            ("La série harmonique Σ 1/n ...",
             [("converge vers 1", False), ("diverge", True), ("converge vers ln 2", False), ("converge vers π²/6", False)]),
        ],
        "Maths"
    )
    
    db.create_quizz(
        [
            ("En quelle année a eu lieu la prise de la Bastille ?",
             [("1776", False), ("1789", True), ("1799", False), ("1804", False)]),
            ("Qui a été couronné empereur à Rome en l'an 800 ?",
             [("Clovis", False), ("Charles Martel", False), ("Charlemagne", True), ("Hugues Capet", False)]),
            ("Dans quelle ville Jeanne d'Arc a-t-elle été brûlée en 1431 ?",
             [("Orléans", False), ("Reims", False), ("Paris", False), ("Rouen", True)]),
            ("Quel roi a fait construire la cour et le château de Versailles comme résidence royale ?",
             [("Louis XIV", True), ("Louis XVI", False), ("François Ier", False), ("Henri IV", False)]),
            ("En quelle année Napoléon Bonaparte devient-il empereur des Français ?",
             [("1799", False), ("1815", False), ("1804", True), ("1792", False)]),
            ("Quelle bataille de 1815 marque la défaite définitive de Napoléon ?",
             [("Austerlitz", False), ("Waterloo", True), ("Iéna", False), ("Trafalgar", False)]),
            ("En quelle année l'esclavage est-il définitivement aboli en France (décret Schœlcher) ?",
             [("1794", False), ("1815", False), ("1870", False), ("1848", True)]),
            ("En quelle année est fondée la Ve République, avec le général de Gaulle ?",
             [("1946", False), ("1958", True), ("1968", False), ("1945", False)]),
        ],
        "Histoire de France"
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
    try:
        quiz_id = int(request.args.get("quiz_id", 0))
        quiz_result = json.loads(request.args.get("quiz_result", "[]"))
    except (ValueError, TypeError, json.JSONDecodeError):
        return "Paramètres de résultat invalides.", 400

    all_quizzes = db.get_all_quiz()
    titre_quiz = next((titre for q_id, titre in all_quizzes if q_id == quiz_id), None)

    correct, total = compute_score(quiz_id, quiz_result)

    username = session.get("username")
    if username:
        id_resultat = db.create_resultat(quiz_id, username)
        if id_resultat is not None:
            for id_rep in quiz_result:
                db.create_aCommeReponse(id_rep, id_resultat)

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



@app.route('/cree', methods=['GET', 'POST'])
def cree():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        admin_key = request.form.get('admin_key', '').strip()

        if not username or not password:
            return render_template('cree.html', error="Veuillez remplir tous les champs obligatoires.")

        if admin_key:
            if admin_key == ADMIN_SECRET_KEY:
                is_admin = True
            else:
                return render_template('cree.html', error="Clé Admin incorrecte!!")
        else:
            is_admin = False

        pass_hash = generate_password_hash(password)
        success = db.create_user(username, pass_hash, is_admin)

        if not success:
            return render_template('cree.html', error="Ce nom d'utilisateur est déjà utilisé.")

        # Log in direct apres creation de compte
        session["username"] = username
        session["isAdmin"] = is_admin
        return redirect(url_for('index'))
    
    return render_template('cree.html')


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
    # Le createur doit etre logged in pour cree un quiz
    if not session.get("username"):
        return redirect(url_for("login"))
    
    # Il doit aussi etre admin 
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
    
@app.route("/historique/<username>")
def hist(username: str):
     # Le createur doit etre logged in pour consulter son history
    if not session.get("username"):
        return redirect(url_for("login"))
    
    username_db = session["username"] 
    
    res = db.get_all_result_from_user(username_db) or []
    history=[]
    for id_res, date, id_quiz in res:
        reponses = db.get_all_reponse_from_resultat(id_res) or []
        lignes = []
        for id_rep, texte_rep, correct, id_question in reponses:
            infos = db.get_question_and_correct(id_question)
            question_text, bonnes = infos if infos else (f"Question {id_question}", [])
            lignes.append({
                'question': question_text,
                'donnee': texte_rep,
                'correct': bool(correct),
                'bonnes': bonnes,
            })
        history.append({'id': id_res, 'date': date, 'quiz': id_quiz, 'reponse': lignes})
        
        
    return render_template("historique.html", history=history)


if __name__ == "__main__":
    app.run(port=5555, debug=False)


