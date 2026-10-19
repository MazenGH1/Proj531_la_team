import sqlite3

connection_db=sqlite3.connect("Quizco.db")
cursor = connection_db.cursor()

if __name__=="__main__":
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Quiz (
            id_quiz INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Question (
            id_question INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            id_quiz INTEGER NOT NULL,
            FOREIGN KEY (id_quiz) REFERENCES Quiz (id_quiz)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reponse (
            id_rep INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            reponse TEXT NOT NULL,
            correct BOOLEAN NOT NULL,
            id_question INTEGER NOT NULL,
            FOREIGN KEY (id_question) REFERENCES Question (id_question)
        )
    """)
    cursor.execute("""
        INSERT INTO Quiz (id_quiz, titre) 
        VALUES 
            (1, "Quiz 1")
    """)
    cursor.execute("""
        INSERT INTO Question (id_question, question, id_quiz) 
        VALUES 
            (1, "Question 1", 1)
    """)
    cursor.execute("""
        INSERT INTO Reponse (id_rep, reponse, correct, id_question)
        VALUES 
            (1, "Oui", True, 1),
            (2, "Non", False, 1)
    """)
    connection_db.commit()


def get_all_quiz()->list[tuple[int, str]]:
    return [(1,"Quiz1")]

def get_qa_from(id_quiz:int)->list[tuple[int, str,list[tuple[int, str,bool]]]]:
    return [(1,"Question 1", [(1,"Oui",True),(2,"Non",False)])]











connection_db.close()