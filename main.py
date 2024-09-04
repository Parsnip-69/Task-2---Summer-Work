from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_bcrypt import Bcrypt
import stripe

stripe.api_key = 'sk_test_51Pv04PP40o7MRH4j3ASKDSgRrLQwVaWqgI8T3GFsBNUnH20cvDFbWjj39trjbEoH3mHVqm1NfvtqWCvZDB4uwzQM00hCHXVShw'

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'password' 

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html", username=session.get('username'))

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

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO personal_details (first_name, last_name , address, city, email) VALUES (?,?,?,?,?)", (first_name, last_name, address, city, email))
                cur.execute("INSERT INTO login_info (username, password) VALUES (?,?)", (username, hashed_password))
                con.commit()
                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = f"Error in insert operation: {e}"
        finally:
            con.close()
            return render_template("result.html", msg=msg)
    else:
        return render_template("join.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT password FROM login_info WHERE username = ?", (username,))
            data = cur.fetchone()
            
            if data:
                stored_password_hash = data[0]
                if bcrypt.check_password_hash(stored_password_hash, password):
                    session['username'] = username  
                    return redirect(url_for('index'))
                else:
                    error = "Invalid username or password"
            else:
                error = "Invalid username or password"
    
    return render_template("login.html", error=error)

@app.route('/account')
def account():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("""
            SELECT pd.firstName, pd.lastName, pd.address, pd.city, pd.email 
            FROM personal_details pd
            JOIN login_info li ON pd.personalID = li.userID
            WHERE li.username = ?
        """, (username,))
        account_data = cur.fetchone()

    if account_data:
        first_name, last_name, address, city, email = account_data
        return render_template("account.html", username=username, first_name=first_name, last_name=last_name, address=address, city=city, email=email)
    else:
        return "Error: Account data not found.", 404

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Baked Goods',  # Customize based on the product
                    },
                    'unit_amount': 500,  # Amount in cents ($5.00)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        return redirect(session.url, code=303)
    except Exception as e:
        return str(e)

@app.route('/success')
def success():
    return "Payment succeeded!"

@app.route('/cancel')
def cancel():
    return "Payment canceled!"


if __name__ == "__main__":
    app.run(debug=True)
