import sqlite3
import bcrypt

# Generate a hashed password
password = 'password'
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
print("Connected to database successfully")

# Drop existing tables
conn.execute('DROP TABLE IF EXISTS login_info')
conn.execute('DROP TABLE IF EXISTS personal_details')
conn.execute('DROP TABLE IF EXISTS table_bookings')
conn.execute('DROP TABLE IF EXISTS table_info')
conn.execute('DROP TABLE IF EXISTS restaurant_info')
conn.execute('DROP TABLE IF EXISTS lesson_bookings')
conn.execute('DROP TABLE IF EXISTS instructor_expertise')
conn.execute('DROP TABLE IF EXISTS lessons_info')
conn.execute('DROP TABLE IF EXISTS type_of_lesson')
conn.execute('DROP TABLE IF EXISTS instructor_info')
print("Dropped all tables successfully")

# Create tables
conn.execute('''
CREATE TABLE personal_details (
    personalID INTEGER PRIMARY KEY,
    firstName TEXT,
    lastName TEXT,
    address TEXT,
    city TEXT,
    email TEXT
)''')
print("Personal Details table created successfully")

conn.execute('''
CREATE TABLE login_info (
    userID INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    personalID INTEGER,
    adminRights BOOLEAN,
    FOREIGN KEY(personalID) REFERENCES personal_details(personalID)
)''')
print("Login Information table created successfully")

conn.execute('''
CREATE TABLE restaurant_info (
    restaurantID INTEGER PRIMARY KEY,
    phoneNumber TEXT,
    email TEXT,
    address TEXT,
    city TEXT
)''')
print("Restaurant Information table created successfully")

conn.execute('''
CREATE TABLE table_info (
    tableID INTEGER PRIMARY KEY,
    restaurantID INTEGER,
    localTableNumber INTEGER,
    FOREIGN KEY(restaurantID) REFERENCES restaurant_info(restaurantID)
)''')
print("Table Information table created successfully")

conn.execute('''
CREATE TABLE table_bookings (
    tableBookingID INTEGER PRIMARY KEY,
    userID INTEGER,
    numberOfPeople INTEGER,
    tableID INTEGER,
    bookingMade DATE,
    DateFor DATE,
    TimeFor TIME,
    lessonID INTEGER,
    FOREIGN KEY(userID) REFERENCES login_info(userID),
    FOREIGN KEY(tableID) REFERENCES table_info(tableID),
    FOREIGN KEY(lessonID) REFERENCES lessons_info(lessonID)
)''')
print("Table Bookings table created successfully")

conn.execute('''
CREATE TABLE lesson_bookings (
    lessonBookingID INTEGER PRIMARY KEY,
    bookingDateAndTime DATETIME,
    userID INTEGER,
    totalAmount REAL,
    lessonID INTEGER,
    FOREIGN KEY(userID) REFERENCES login_info(userID),
    FOREIGN KEY(lessonID) REFERENCES lessons_info(lessonID)
)''')
print("Lesson Bookings table created successfully")

conn.execute('''
CREATE TABLE instructor_info (
    instructorID INTEGER PRIMARY KEY,
    personalID INTEGER,
    FOREIGN KEY(personalID) REFERENCES personal_details(personalID)
)''')
print("Instructor Info table created successfully")

conn.execute('''
CREATE TABLE lessons_info (
    lessonID INTEGER PRIMARY KEY,
    instructorID INTEGER,
    restaurantID INTEGER,
    dateOfLesson DATE,
    numberOfPlaces INTEGER,
    lessonTypeID INTEGER,
    FOREIGN KEY(instructorID) REFERENCES instructor_info(instructorID),
    FOREIGN KEY(restaurantID) REFERENCES restaurant_info(restaurantID),
    FOREIGN KEY(lessonTypeID) REFERENCES type_of_lesson(lessonTypeID)
)''')
print("Lessons Info table created successfully")

conn.execute('''
CREATE TABLE type_of_lesson (
    lessonTypeID INTEGER PRIMARY KEY,
    titleOfLesson TEXT,
    costOfLesson REAL
)''')
print("Type of Lesson table created successfully")

conn.execute('''
CREATE TABLE instructor_expertise (
    qualificationID INTEGER PRIMARY KEY,
    instructorID INTEGER,
    lessonTypeID INTEGER,
    FOREIGN KEY(instructorID) REFERENCES instructor_info(instructorID),
    FOREIGN KEY(lessonTypeID) REFERENCES type_of_lesson(lessonTypeID)
)''')
print("Instructor Expertise table created successfully")

# Insert test data
conn.execute('''
INSERT INTO personal_details (firstName, lastName, address, city, email)
VALUES ('Bob', 'Smith', '123 Main Street', 'Cardiff', 'bob.smith@email.com')
''')

conn.execute('''
INSERT INTO login_info (username, password, personalID, adminRights)
VALUES ('bob.smith', ?, 1, 0)''', (hashed_password,))
print("Added test data into login_info & personal_details tables successfully")

# Commit the changes and close the connection
conn.commit()
conn.close()
print("Disconnected from database successfully")
