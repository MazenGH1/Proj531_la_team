import sqlite3

connection_db=sqlite3.connect("Quizco.db")
cursor = connection_db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Quiz (
        id_quiz INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL
    )
    
    CREATE TABLE IF NOT EXISTS Question (
        id_question INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        id_quiz INTEGER NOT NULL
    )
    
    CREATE TABLE IF NOT EXISTS Reponse (
        id_rep INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        reponse TEXT NOT NULL,
        id_question INTEGER NOT NULL
    )
        
    
""")

def get_all_quiz()->list[tuple[int, str]]:
    return [(1,"Quiz1")]

def get_qa_from(id_quiz:int)->list[tuple[int, str,list[tuple[int, str,bool]]]]:
    return [(1,"Question 1", [(1,"Oui",True),(2,"Non",False)])]











connection_db.close()