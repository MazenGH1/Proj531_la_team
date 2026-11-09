import os
import sqlite3

TABLES_AUTORISE = {
    "Quiz",
    "Question",
    "Reponse",
    "Utilisateur",
    "Resultat",
    "aCommeReponse",
}

# NE PAS TOUCHER CA !!
BDD_CHEMIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Quizco.db")


def get_sql_connection() -> sqlite3.Connection:
    return sqlite3.connect(BDD_CHEMIN)


def get_max_id(table: str) -> int:
    if table not in TABLES_AUTORISE:
        raise ValueError(f"Invalid table name: {table}")

    query = f"SELECT MAX(id) FROM {table}"
    res = 0
    try:
        with get_sql_connection() as connection_db:
            cursor_db = connection_db.cursor()
            cursor_db.execute(query)
            row = cursor_db.fetchone()
            if row and row[0] is not None:
                res = row[0]
    except sqlite3.Error as error:
        print(f"Error dans la BDD: {error}")
    return res


def init_BDD() -> None:
    """
    Creates the BDD, does nothing if already exists
    """
    try:
        with get_sql_connection() as connection_db:
            cursor = connection_db.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS Quiz
                           (
                               id
                               INTEGER
                               NOT
                               NULL
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               titre
                               TEXT
                               NOT
                               NULL
                           )
                           ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS Question
                           (
                               id
                               INTEGER
                               NOT
                               NULL
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               question
                               TEXT
                               NOT
                               NULL,
                               id_quiz
                               INTEGER
                               NOT
                               NULL,
                               FOREIGN
                               KEY
                           (
                               id_quiz
                           ) REFERENCES Quiz
                           (
                               id
                           )
                               )
                           ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS Reponse
                           (
                               id
                               INTEGER
                               NOT
                               NULL
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               reponse
                               TEXT
                               NOT
                               NULL,
                               correct
                               BOOLEAN
                               NOT
                               NULL,
                               id_question
                               INTEGER
                               NOT
                               NULL,
                               FOREIGN
                               KEY
                           (
                               id_question
                           ) REFERENCES Question
                           (
                               id
                           )
                               )
                           ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS Utilisateur
                           (
                               username
                               TEXT
                               NOT
                               NULL
                               PRIMARY
                               KEY,
                               passHash
                               TEXT
                               NOT
                               NULL,
                               isAdmin
                               BOOLEAN
                               NOT
                               NULL
                           )
                           ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS Resultat
                           (
                               id
                               INTEGER
                               NOT
                               NULL
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               dateHeure
                               TIMESTAMP
                               NOT
                               NULL,
                               username
                               TEXT
                               NOT
                               NULL,
                               id_quiz
                               INTEGER
                               NOT
                               NULL,
                               FOREIGN
                               KEY
                           (
                               id_quiz
                           ) REFERENCES Quiz
                           (
                               id
                           ),
                               FOREIGN KEY
                           (
                               username
                           ) REFERENCES Utilisateur
                           (
                               username
                           )
                               )
                           ''')
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS aCommeReponse
                           (
                               id_res
                               INTEGER
                               NOT
                               NULL,
                               id_rep
                               INTEGER
                               NOT
                               NULL,
                               PRIMARY
                               KEY
                           (
                               id_rep,
                               id_res
                           ),
                               FOREIGN KEY
                           (
                               id_rep
                           ) REFERENCES Reponse
                           (
                               id
                           ),
                               FOREIGN KEY
                           (
                               id_res
                           ) REFERENCES Resultat
                           (
                               id
                           )
                               )
                           ''')
    except sqlite3.Error as error:
        print(error)
    finally:
        connection_db.commit()
        connection_db.close()


def get_all_quiz() -> list[tuple[int, str]]:
    """
    returns a list of all quizzes id and title
    """
    res = []
    try:
        with get_sql_connection() as connection_gaq:
            cursor_gaq = connection_gaq.cursor()

            cursor_gaq.execute("SELECT * FROM Quiz")
            quizzes = cursor_gaq.fetchall()
            for row in quizzes:
                res.append((row[0], row[1]))

    except sqlite3.Error as error:
        print(error)
    finally:
        connection_gaq.close()
    return res


def get_qa_from(id_quiz: int) -> list:
    res = []
    connection = None
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, question FROM Question WHERE id_quiz = ?",
            (id_quiz,)
        )
        questions = cursor.fetchall()

        for id_question, question in questions:
            cursor.execute(
                """
                SELECT id, reponse, correct
                FROM Reponse
                WHERE id_question = ?
                """,
                (id_question,)
            )
            responses = cursor.fetchall()

            reponses = [
                (id_rep, texte_rep, bool(correct))
                for id_rep, texte_rep, correct in responses
            ]

            res.append((id_question, question, reponses))

        return res

    except sqlite3.Error as e:
        print(f"Database error in get_qa_from: {e}")
        raise
    finally:
        # This guarantees the file unlocks
        if connection:
            connection.close()


def create_quizz(quiz: list[tuple[str, list[tuple[str, bool]]]], titre: str) -> None:
    conn = None
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Quiz (titre) VALUES (?)", (titre,))
        id_quiz = cursor.lastrowid

        for texte_question, reponses in quiz:
            create_question(texte_question, reponses, id_quiz, conn)

        conn.commit()
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        raise
    finally:
        # This guarantees the file unlocks
        if conn:
            conn.close()

def create_question(question : str, reponses : list[tuple[str, bool]], id_quiz : int|None, conn = None) -> None:
    has_conn = True
    try :
        if conn is None:
            conn = get_sql_connection()
            has_conn = False
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Question (question, id_quiz) VALUES (?, ?)", (question, id_quiz))
        id_question = cursor.lastrowid

        for texte_rep, correct in reponses:
            create_reponse(texte_rep, correct, id_question, conn)

        conn.commit()
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        raise
    finally:
        if conn and not has_conn:
            conn.close()

def create_reponse(message : str, correct: bool, id_quest : int|None, conn = None) -> None:
    has_conn = True
    try :
        if conn is None:
            conn = get_sql_connection()
            has_conn = False
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Reponse (reponse, correct, id_question) VALUES (?, ?, ?)", (message, correct, id_quest))

        conn.commit()
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        raise
    finally:
        if conn and not has_conn:
            conn.close()




def create_user(username: str, pass_hash: str, is_admin: bool = False) -> bool:
    query = """
            INSERT INTO Utilisateur (username, passHash, isAdmin)
            VALUES (?, ?, ?) \
            """
    try:
        with get_sql_connection() as conn:
            cursor = conn.cursor()
            # Les parametres sont en tuples
            cursor.execute(query, (username, pass_hash, is_admin))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        # Username existe deja
        return False
    except sqlite3.Error as error:
        print(f"Erreur dans BDD: {error}")
        return False
    finally:
        if conn:
            conn.close()


def get_user_by_username(username: str) -> tuple[str, str, bool] | None:
    query = "SELECT username, passHash, isAdmin FROM Utilisateur WHERE username = ?"
    try:
        with get_sql_connection() as conn:
            cursor = conn.cursor()
            # SQLite treats the 'username' string strictly as data, not executable code
            cursor.execute(query, (username,))
            return cursor.fetchone()
    except sqlite3.Error as error:
        print(f"Erreur dans BDD: {error}")
        return None
    finally:
        if conn:
            conn.close()

def create_resultat(id_quiz: int, username: str) -> bool:
    query = """
            INSERT INTO Resultat (id_quiz, username, dateHeure)
            VALUES (?, ?, CURRENT_TIMESTAMP)          
            """
    try:
        with get_sql_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id_quiz, username))
            conn.commit()
            return True
    except sqlite3.Error as error:
        print(f"Erreur dans BDD: {error}")
        return False
    finally:
        if conn:
            conn.close()

def create_aCommeReponse(id_reponse: int, id_resultat: int) -> bool:
    query = """
            INSERT INTO aCommeReponse (id_rep, id_res)
            VALUES (?, ?) \
            """
    try:
        with get_sql_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id_reponse,id_resultat))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print("question deja repondu dans cette session")
        return False
    except sqlite3.Error as error:
        print(f"Erreur dans BDD: {error}")
        return False
    finally:
        if conn:
            conn.close()

def get_all_reponse_from_resultat(id_resultat: int) -> list[tuple[int,str, bool, int]] | None:
    """
    :return: list[tuple[id_reponse, reponse, correct, id_question]]
    """
    query = """
            SELECT id, reponse, correct, id_question FROM Reponse
            JOIN aCommeReponse ON Reponse.id = aCommeReponse.id_rep
            WHERE aCommeReponse.id_res = ?
            """
    try:
        with get_sql_connection() as conn:
            res = []
            cursor = conn.cursor()
            cursor.execute(query, (id_resultat,))
            for line in cursor.fetchall():
                res.append((line[0],line[1],line[2],line[3]))
            return res
    except sqlite3.Error as error:
        print(f"Erreur dans BDD: {error}")
        return None

def get_all_result_from_user(username : str) -> list[tuple[int, str, int]] | None:
    """
    :return: list[tuple[id_resultat, dateHeure, id_quiz]]
    """
    query = """
            SELECT id, dateHeure, id_quiz FROM Resultat
            WHERE username = ?
            """
    try:
        with get_sql_connection() as conn:
            res = []
            cursor = conn.cursor()
            cursor.execute(query, (username,))
            for line in cursor.fetchall():
                res.append((line[0],line[1],line[2]))
            return res
    except sqlite3.Error as error:
        print(f"Erreur dans BDD: {error}")
        return None




if __name__ == "__main__":
    init_BDD()
    existing_quizzes = get_all_quiz()
    if len(existing_quizzes) == 0:
        print("Database empty! Inserting sample quiz...")
        create_quizz(
            [
                ("Quelle est la capitale de la Suisse ?",
                 [("Berne", True), ("Genève", False), ("Bâle", False)]),
                ("Combien font 7+7 ?",
                 [("13", False), ("14", True), ("15", False)]),
            ],
            "Quiz 1"
        )
        create_user("Robert", "oUsItItI", True)
        create_user("Alban", "244466666", False)
        create_user("Frederic EricFred", "baheoyghluqvsjdfkbnphate^r£ZQFJ", True)
    else:
        print("Quiz already exists in database.")

    print("Tous les quiz :", get_all_quiz())
    print("Questions du quiz 1 :", get_qa_from(1))
    print("Resultats :", get_all_reponse_from_resultat(1))
    #print(get_all_reponse_from_resultat(1))
    create_user("Robert", "oUsItItI", True)
    create_user("Alban", "244466666", False)
    #
    create_resultat(1, "Alban")
    create_aCommeReponse(1, 1)
    create_aCommeReponse(5, 1)
    print(get_all_result_from_user("Alban"))