import mysql.connector



dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Saruar2207!'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE elderco")

print("ALL done!")