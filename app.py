from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
import sqlite3


app = Flask(__name__)
app.secret_key = "Secret Key"

#crea la base de datos y la conexion a la base de datos sqlite
conexion = sqlite3.connect('database/eccomerce.db', check_same_thread=False)
cursor = conexion.cursor()
conexion.commit()













@app.route('/')
@app.route('/index')
@app.route('/inicio')
def index():
    return render_template('inicio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        if not (correo and contrasena):
            flash("Rellene todos los campos")
            return redirect(url_for('login'))
        else:
            correo = correo.strip()
            contrasena = contrasena.strip()
        cursor.execute("SELECT * FROM usuarios WHERE correo=? AND contrasena=?", (correo,contrasena))
        filas = cursor.fetchone()

        if not filas:
            flash("Correo o contrasena incorrectos")
        else:
            return render_template("inicio.html", nombre = filas)
            return redirect(url_for('index'))
    return render_template('login.html')
        

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        pais = request.form['pais']

        if not (nombre and contrasena):
            flash("Rellene todos los campos")
            return redirect(url_for('registro'))
        else:
            nombre = nombre.strip()
            apellido = apellido.strip()
            correo = correo.strip()
            contrasena = contrasena.strip()
            pais = pais.strip()
        
        cursor.execute("INSERT INTO usuarios(nombre,apellido,correo,contrasena,pais,id_rol) VALUES (?,?,?,?,?,?)", (nombre,apellido,correo,contrasena,pais,1))
        conexion.commit()
        flash("Cuenta creada exitosamente")
        return redirect(url_for('login'))
    return render_template("registro.html")





@app.route('/producto', methods=['GET'])
def producto():
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    filas = cursor.fetchall()
    return render_template("producto.html", filas = filas)


@app.route('/productodetalle/<id>', methods=['GET'])
def productodetalle(id):
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id=?", id)
    filas = cursor.fetchall()
    return render_template("producto-detalle.html", filas = filas)


@app.route('/favoritos', methods=['GET'])
def favoritos():
    return render_template('favoritos.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    filas = cursor.fetchall()
    return render_template("admin.html", filas = filas)



@app.route('/admin_usuarios', methods=['GET', 'POST'])
def admin_usuarios():
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios")
    filas = cursor.fetchall()
    if (filas[1] == 2):
        filas[1] = 'Administrador'
    return render_template("admin-usuarios.html", filas = filas)


@app.route('/actualizar_usuario', methods=['GET', 'POST'])
def actualizar_usuario():
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        pais = request.form['pais']
        rol = request.form['rol']
        cursor.execute("UPDATE usuarios SET nombre = ?, apellido = ?, correo = ?, pais = ?, id_rol = ? WHERE id = ?", (nombre,apellido,correo,pais,rol,id))
        conexion.commit()
        flash("Usuario Actualizado Exitosamente")
        return redirect(url_for('admin_usuarios'))



@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        estado = request.form['estado']
        imagen = request.form['imagen']
        cursor.execute("INSERT INTO productos(nombre,precio,descripcion,cantidad,estado,imagen) VALUES (?,?,?,?,?,?)", (nombre,precio,descripcion,cantidad,estado,imagen))
        conexion.commit()
        flash("Producto Agregado Exitosamente")
        return redirect(url_for('admin'))



@app.route('/actualizar_producto', methods=['GET', 'POST'])
def actualizar_producto():
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        estado = request.form['estado']
        imagen = request.form['imagen']
        cursor.execute("UPDATE productos SET nombre = ?, precio = ?, descripcion = ?, cantidad = ?, estado = ?, imagen = ? WHERE id = ?", (nombre,precio,descripcion,cantidad,estado,imagen,id))
        conexion.commit()
        flash("Producto Actualizado Exitosamente")
        return redirect(url_for('admin'))




@app.route('/eliminar_producto/<id>/', methods=['GET', 'POST'])
def eliminar_producto(id):
    int(id)
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    conexion.commit()
    flash("Producto Eliminado Exitosamente")
    return redirect(url_for('admin'))




if __name__ == '__main__':
    app.run(debug=True)