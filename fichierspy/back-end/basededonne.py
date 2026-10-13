import sqlite3

connectiondb=sqlite3.connect("Quizco.db")
cursor = connectiondb.cursor()

connectiondb.close()