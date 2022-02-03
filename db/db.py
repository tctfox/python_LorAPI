import sqlite3

cardSearchName = "Pyke"

connection = sqlite3.connect("Cards.db")
cursor = connection.cursor()
cursor.execute(f"SELECT * from cards WHERE name like '%{cardSearchName}%'")
results = cursor.fetchall()


for currentcard in results:
    print(currentcard)

connection.close()

