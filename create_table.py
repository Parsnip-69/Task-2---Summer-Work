import sqlite3


conn = sqlite3.connect('database.db')
#print("Connected to database successfully")

conn.execute('DROP TABLE personal_details')
conn.execute('DROP TABLE login_info')
print("Dropped all tables successfully")

conn.execute('CREATE TABLE personal_details (personalID INTEGER PRIMARY KEY ,first_name TEXT, last_name TEXT, address TEXT, city TEXT, email TEXT)')
print("Personal Detail's table created successfully")

conn.execute('CREATE TABLE login_info (userID INTEGER PRIMARY KEY, username TEXT, password TEXT, FOREIGN KEY(userID) REFERENCES personal_details(personalID))')
print("Login Information's table created successfully")



conn.close()
print("Disconnected from database successfully")