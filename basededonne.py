import sqlite3


TABLES_AUTORISE = {
    "Quiz",
    "Question",
    "Reponse",
    "Utilisateur",
    "Resultat",
    "aCommeReponse",
}


def get_sql_connection() -> sqlite3.Connection:
    return sqlite3.connect("Quizco.db")

def get_max_id(table : str)->int:
    """
    returns the max id of table
    """
    query = "SELECT MAX(id) FROM {table}".format(table=table)
    res = 0
    try:
        with get_sql_connection() as connection_db:
            cursor_db = connection_db.cursor()
            cursor_db.execute(query)
            res = cursor_db.fetchone()[0]
            if res is None:
                res = 0
    except sqlite3.Error as error:
        print(error)
    finally:
        connection_db.close()
    return res

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



def init_BDD()->None:
    """
    Creates the BDD, does nothing if already exists
    """
    try:
        with get_sql_connection() as connection_db:
            cursor = connection_db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Quiz (
                    id INTEGER NOT NULL PRIMARY KEY,
                    titre TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Question (
                    id INTEGER NOT NULL PRIMARY KEY,
                    question TEXT NOT NULL,
                    id_quiz INTEGER NOT NULL,
                    FOREIGN KEY (id_quiz) REFERENCES Quiz (id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Reponse (
                    id INTEGER NOT NULL PRIMARY KEY,
                    reponse TEXT NOT NULL,
                    correct BOOLEAN NOT NULL,
                    id_question INTEGER NOT NULL,
                    FOREIGN KEY (id_question) REFERENCES Question (id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Utilisateur (
                    username TEXT NOT NULL PRIMARY KEY,
                    passHash TEXT NOT NULL,
                    isAdmin BOOLEAN NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Resultat (
                    id INTEGER NOT NULL PRIMARY KEY,
                    dateHeure TIMESTAMP NOT NULL,
                    username TEXT NOT NULL,
                    id_quiz INTEGER NOT NULL,
                    FOREIGN KEY (id_quiz) REFERENCES Quiz (id)
                    FOREIGN KEY (username) REFERENCES Utilisateur (username)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS aCommeReponse (
                    id_res INTEGER NOT NULL,
                    id_rep INTEGER NOT NULL,
                    PRIMARY KEY (id_rep, id_res)
                    FOREIGN KEY (id_rep) REFERENCES Reponse (id)
                    FOREIGN KEY (id_res) REFERENCES Resultat (id)
                )
            ''')
    except sqlite3.Error as error:
        print(error)
    finally:
        connection_db.commit()
        connection_db.close()


def get_all_quiz()->list[tuple[int, str]]:
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

def get_qa_from(id_quiz:int)->list[tuple[int, str,list[tuple[int, str,bool]]]]:
    """
    returns list[tuple(id_question, question, list[tuple(id_reponse, reponse, correct)])]
    """
    res = []
    try:
        with get_sql_connection() as connection_gqf:
            cursor_gqf = connection_gqf.cursor()
            cursor_gqf.execute("SELECT * FROM Question WHERE id_quiz = ?", (id_quiz,))
            questions = cursor_gqf.fetchall()
            for row in questions:
                id_question = row[0]
                question = row[1]
                rep = []
                cursor_gqf.execute("SELECT * FROM Reponse WHERE id_question = ?", (id_question,))
                responses = cursor_gqf.fetchall()
                for row1 in responses:
                    rep.append((row1[0], row1[1], row1[2]))
                res.append((id_question, question, rep))
    except sqlite3.Error as error:
        print(error)
    finally:
        connection_gqf.close()
    return res


def create_quizz(quiz: list[tuple[str, list[tuple[str, bool]]]], titre: str) -> None:
    try:
        with get_sql_connection() as connection_cq:
            cursor = connection_cq.cursor()
            cursor.execute('''
                INSERT INTO Quiz (titre)
                VALUES
                    (titre)
            ''')
            id_quiz = get_max_id("Quiz")
            for question in quiz:
                cursor.execute('''
                    INSERT INTO Question (question, id_quiz)
                    VALUES 
                        (question[0],id_quiz)
                ''')
                id_question = get_max_id("Question")
                for reponse in question[1]:
                    cursor.execute('''
                    INSERT INTO Reponse (reponse, correct, id_question)
                    VALUES 
                        (reponse[0], reponse[1], id_question)
                    ''')
    except sqlite3.Error as error:
        print(error)
    finally:
        connection_cq.close()
        
        
def create_user(username: str, pass_hash: str, is_admin: bool = False) -> bool:
    query = """
        INSERT INTO Utilisateur (username, passHash, isAdmin)
        VALUES (?, ?, ?)
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





if __name__=="__main__":
    init_BDD()
    print(get_all_quiz())
    print(get_qa_from(1))
    print(get_max_id("Quiz"))
    print(get_max_id("Resultat"))

if __name__ == "__main__" and False:
    connection_test = sqlite3.connect("Quizco.db")
    cursor_test = connection_test.cursor()

    cursor_test.execute('''
        INSERT INTO Quiz (titre)
        VALUES
            ("Quiz 1")
     ''')
    cursor_test.execute('''
        INSERT INTO Question (question, id_quiz)
        VALUES
            ("Question 1", 1)
     ''')
    cursor_test.execute('''
        INSERT INTO Reponse (reponse, correct, id_question)
        VALUES
            ("Oui", True, 1),
            ("Non", False, 1)
     ''')
#    cursor_test.execute('''
#        INSERT INTO Utilisateur (username, passHash, isAdmin)
#        VALUES
#            ("Robert", "oUsItItI", True),
#            ("Alban", "244466666", False)
#        ''')
    cursor_test.execute('''
        INSERT INTO Resultat (dateHeure, username, id_quiz)
        VALUES
            (current_timestamp, "Alban", 1)
        ''')
#    cursor_test.execute('''
#        INSERT INTO aCommeReponse (id_res, id_rep)
#        VALUES
#            (1, 1)
#    ''')

    connection_test.commit()
    connection_test.close()
