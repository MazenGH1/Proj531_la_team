import sqlite3

def get_sql_connection() -> sqlite3.Connection:
    return sqlite3.connect("Quizco.db")

def get_max_id(table : str)->int:
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



def init_BDD():
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
