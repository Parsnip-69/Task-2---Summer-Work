from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from flask_bcrypt import Bcrypt
import stripe

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'password'

# Set up your secret Stripe API key
stripe.api_key = 'sk_test_51Pv04PP40o7MRH4j3ASKDSgRrLQwVaWqgI8T3GFsBNUnH20cvDFbWjj39trjbEoH3mHVqm1NfvtqWCvZDB4uwzQM00hCHXVShw'

# Set your domain
YOUR_DOMAIN = 'http://localhost:5000'

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html", username=session.get('username'))

@app.route('/coffee')
def coffee():
    return render_template("coffee.html", username=session.get('username'))

@app.route('/bakedgoods')
def baked():
    return render_template("baked.html", username=session.get('username'))

@app.route('/lessons')
def lessons():
    return render_template("lessons.html", username=session.get('username'))

@app.route('/tables')
def tables():
    return render_template("tables.html", username=session.get('username'))

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
                cur.execute("INSERT INTO personal_details (firstName, lastName, address, city, email) VALUES (?,?,?,?,?)", 
                            (first_name, last_name, address, city, email))
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
            JOIN login_info li ON pd.rowid = li.rowid
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

# Stripe Payment Routes



@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    data = request.json
    amount = data.get('amount')
    customer_name = data.get('customer_name')
    customer_email = data.get('customer_email')

    if 'username' in session:
        username = session['username']

        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                # Retrieve email from the database based on the logged-in user's username
                cur.execute("""
                    SELECT pd.email
                    FROM personal_details pd
                    JOIN login_info li ON pd.personalID = li.personalID
                    WHERE li.username = ?
                """, (username,))
                result = cur.fetchone()
                if result:
                    customer_email = result[0]  # Use the email from the database if available
        except Exception as e:
            return jsonify({'error': f"Error retrieving email from database: {e}"}), 400

    if not customer_email:
        return jsonify({'error': 'Email address is required'}), 400

    # Create a PaymentIntent with the specified amount
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount),
            currency='gbp',
            payment_method_types=['card'],
            receipt_email=customer_email,  # Attach the customer's email to the payment intent
            metadata={'name': customer_name}
        )
        return jsonify({
            'clientSecret': payment_intent.client_secret
        })
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(port=5000, debug=True)
