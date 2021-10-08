from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/inicio')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')