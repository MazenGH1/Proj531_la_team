import sqlite3

connection_db=sqlite3.connect("Quizco.db")
cursor = connection_db.cursor()



def get_all_quiz()->list[tuple[int, str]]:
    return [(1,"Quiz1")]

def get_qa_from(id_quiz:int)->list[tuple[int, str,list[tuple[int, str,bool]]]]:
    return [(1,"Question 1", [(1,"Oui",True),(2,"Non",False)])]











connection_db.close()