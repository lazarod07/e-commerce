from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "Secret Key"

#crea la base de datos y la conexion a la base de datos sqlite
conexion = sqlite3.connect('database/eccomerce.db', check_same_thread=False)
cursor = conexion.cursor()
conexion.commit()





@app.before_request
def verificar():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if not 'usuario' in session and ruta != "/login" and ruta != "/loguear" and ruta != "/registro" and not ruta.startswith("/static"):
        flash("Inicia sesión para continuar")
        return redirect("/login")











@app.route('/')
@app.route('/index')
@app.route('/inicio')
def index():
    return render_template('inicio.html')




@app.route("/login")
def login():
    return render_template("login.html")



@app.route('/cerrar_session')
def cerrar_session():
    session.clear()
    return redirect(url_for('login'))


@app.route('/loguear', methods=['POST'])
def loguear():
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
            session["usuario"] = filas[1]
            session["id"] = filas[0]
            session["rol"] = filas[6]
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




@app.route('/comentar', methods=['POST'])
def comentar():
    if request.method == 'POST':
        id = request.form['identificador']
        comentario = request.form['comentario']
        idusuario = session['id']
        fecha = datetime.today().strftime('%Y-%m-%d %H:%M')
        cursor.execute("INSERT INTO comentarios(usuario, id_producto, comentario, fecha) VALUES (?,?,?,?)", (session["usuario"], id, comentario, fecha))
        conexion.commit()
    return redirect(url_for('producto'))
    #return redirect(url_for('productodetalle/<id>'))









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
    session["identificador"] = id
    #cursor.execute("SELECT * FROM productos, comentarios WHERE productos.id=? AND  comentarios.id_producto=? LIMIT 2", (id,id))
    cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
    producto = cursor.fetchall()
    cursor.execute("SELECT usuario, id_producto, comentario, fecha FROM comentarios WHERE id_producto=?", (id,))
    comentarios = cursor.fetchall()
    producto.extend(comentarios)
    del producto[0]
    #producto = comentarios
    return render_template("producto-detalle.html", filas = producto)



@app.route('/favoritos')
def favoritos():
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    idusuario = session['id']
    cursor.execute("SELECT productos.id, productos.nombre, productos.precio FROM productos, favoritos WHERE favoritos.id_producto = productos.id AND favoritos.id_usuario = ?", (idusuario,))
    filas = cursor.fetchall()
    return render_template("favoritos.html", filas = filas)





@app.route('/agregar_favoritos/<id>', methods=['GET'])
def agregar_favoritos(id):
    idusuario = session['id']
    cursor.execute("INSERT INTO favoritos(id_usuario, id_producto) VALUES (?,?)", (idusuario, id))
    conexion.commit()
    return redirect(url_for('producto'))



@app.route('/eliminar_favorito/<id>', methods=['GET'])
def eliminar_favorito(id):
    idusuario = session['id']
    cursor.execute("DELETE FROM favoritos WHERE id_usuario=? AND id_producto=?", (idusuario, id))
    conexion.commit()
    return redirect(url_for('favoritos'))




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