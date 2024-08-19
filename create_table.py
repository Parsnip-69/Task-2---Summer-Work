import sqlite3
import bcrypt

# Generate a hashed password
password = 'password'
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
print("Connected to database successfully")

# Drop existing tables
conn.execute('DROP TABLE IF EXISTS personal_details')
conn.execute('DROP TABLE IF EXISTS login_info')
conn.execute('DROP TABLE IF EXISTS tables_info')
conn.execute('DROP TABLE IF EXISTS restaurants_info')
print("Dropped all tables successfully")

# Create tables
conn.execute('''CREATE TABLE personal_details (personalID INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, address TEXT, city TEXT, email TEXT)''')
print("Personal Details table created successfully")

conn.execute('''CREATE TABLE login_info (userID INTEGER PRIMARY KEY, username TEXT, password TEXT,FOREIGN KEY(userID) REFERENCES personal_details(personalID))''')
print("Login Information table created successfully")

conn.execute('''CREATE TABLE restaurants_info (restaurantsID INTEGER PRIMARY KEY, phoneNumber TEXT, email TEXT, address TEXT, city TEXT)''')
print("Restaurants Information table created successfully")

conn.execute('''
CREATE TABLE tables_info (tableID INTEGER PRIMARY KEY, restaurantsID INTEGER, localTableNumber INTEGER, FOREIGN KEY(restaurantsID) REFERENCES restaurants_info(restaurantsID))''')
print("Table Information table created successfully")

# Insert test data
conn.execute('''
INSERT INTO personal_details (first_name, last_name, address, city, email)
VALUES ('Bob', 'Smith', '123 Main Street', 'Cardiff', 'bob.smith@email.com')
''')

conn.execute('''
INSERT INTO login_info (username, password)
VALUES ('bob.smith', ?)
''', (hashed_password,))
print("Added test data into login_info & personal_details tables successfully")

# Commit the changes and close the connection
conn.commit()
conn.close()
print("Disconnected from database successfully")
