import sqlite3

if __name__=="__main__":
    connection_db = sqlite3.connect("Quizco.db")
    cursor = connection_db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Quiz (
            id_quiz INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Question (
            id_question INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            id_quiz INTEGER NOT NULL,
            FOREIGN KEY (id_quiz) REFERENCES Quiz (id_quiz)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reponse (
            id_rep INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            reponse TEXT NOT NULL,
            correct BOOLEAN NOT NULL,
            id_question INTEGER NOT NULL,
            FOREIGN KEY (id_question) REFERENCES Question (id_question)
        )
    ''')
    cursor.execute('''
        INSERT INTO Quiz (titre)
        VALUES
            ("Quiz 1")
     ''')
    cursor.execute('''
        INSERT INTO Question (question, id_quiz)
        VALUES
            ("Question 1", 1)
     ''')
    cursor.execute('''
        INSERT INTO Reponse (reponse, correct, id_question)
        VALUES
            ("Oui", True, 1),
            ("Non", False, 1)
     ''')
    connection_db.commit()
    connection_db.close()

def get_sql_connection() -> sqlite3.Connection:
    return sqlite3.connect("Quizco.db")


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
    print(get_all_quiz())
    print(get_qa_from(1))


