from flask import Flask, render_template, request
import sqlite3
from flask_bcrypt import Bcrypt 

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/aboutus')
def about():
    return render_template("about.html")

@app.route('/coffee')
def coffee():
    return render_template("coffee.html")

@app.route('/bakedgoods')
def baked():
    return render_template("baked.html")

@app.route('/lessons')
def lessons():
    return render_template("lessons.html")

@app.route('/tables')
def tables():
    return render_template("tables.html")

@app.route('/join', methods=['POST', 'GET'])
def join():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            address = request.form['address']
            city = request.form['city']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']

            hashed_password = bcrypt.generate_password_hash (password).decode('utf-8') 
            #is_valid = bcrypt.check_password_hash (hashed_password, password) 
            #return f"Password: {password}<br>Hashed Password: {hashed_password}<br>Is Valid: {is_valid}"


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO personal_details (first_name, last_name , address, city, email) VALUES (?,?,?,?,?)", (first_name, last_name, address, city, email))
                cur.execute("INSERT INTO login_info (username, password) VALUES (?,?)", (username, hashed_password))
                con.commit()
                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = f"Error in insert operation: {str(e)}"
        finally:
            con.close()
            return render_template("result.html", msg=msg)
    else:
        return render_template("join.html")

@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
