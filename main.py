from flask import Flask, render_template

app = Flask (__name__)

@app.route('//<name>')
@app.route('/home/<name>')
def index(name):
    return render_template("index.html", user = name)

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



app.run(debug=True)