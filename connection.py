import mysql.connector
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="user"
    )

# mycursor.execute("CREATE DATABASE user")
# mycursor.execute("CREATE TABLE data (id int AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255), image VARCHAR(255),about VARCHAR(255))")
