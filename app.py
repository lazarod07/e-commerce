from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/inicio')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template('registro.html')

@app.route('/producto', methods=['GET'])
def producto():
    return render_template('producto.html')

@app.route('/productodetalle', methods=['GET'])
def productodetalle():
    return render_template('producto-detalle.html')

@app.route('/favoritos', methods=['GET'])
def favoritos():
    return render_template('favoritos.html')