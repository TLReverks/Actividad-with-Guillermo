import os
import re
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, send_file
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from database.conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "adso2026"

# Carpeta donde se guardan las imágenes de los productos
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
EXTENSIONES_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "webp"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Patrón para el código de producto: P001, P002, P003...
PATRON_CODIGO = re.compile(r"^P\d{3,}$")


def archivo_permitido(nombre_archivo):
    return "." in nombre_archivo and \
        nombre_archivo.rsplit(".", 1)[1].lower() in EXTENSIONES_PERMITIDAS


# ------------------------------------------------------------------
# Decoradores de control de acceso (RBAC)
# ------------------------------------------------------------------
def login_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario" not in session:
            flash("Debe iniciar sesión para continuar.", "warning")
            return redirect(url_for("inicio"))
        return vista(*args, **kwargs)
    return envoltura


def admin_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario" not in session:
            flash("Debe iniciar sesión para continuar.", "warning")
            return redirect(url_for("inicio"))
        if session.get("rol") != "Administrador":
            flash("No tiene permisos para acceder a esa sección.", "danger")
            return redirect(url_for("cliente"))
        return vista(*args, **kwargs)
    return envoltura


def cliente_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario" not in session:
            flash("Debe iniciar sesión para continuar.", "warning")
            return redirect(url_for("inicio"))
        if session.get("rol") != "Cliente":
            # Si un administrador intenta entrar a /cliente, se bloquea
            # y se redirige al panel principal.
            flash("No tiene permisos para acceder a esa sección.", "danger")
            return redirect(url_for("inicio"))
        return vista(*args, **kwargs)
    return envoltura


# ------------------------------------------------------------------
# Páginas públicas
# ------------------------------------------------------------------
@app.route("/")
def inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("index1.html", productos=productos)


@app.route("/catalogo")
def catalogo():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("catalogo.html", productos=productos)


@app.route("/contacto")
def contacto():
    return render_template("contacto.html")


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@app.route("/servicios")
def servicios():
    return render_template("servicios.html")


# ------------------------------------------------------------------
# Autenticación
# ------------------------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    correo = request.form["correo"].strip()
    password = request.form["password"]

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT * FROM usuarios WHERE correo=%s AND estado='Activo'
    """
    cursor.execute(sql, (correo,))
    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario and check_password_hash(usuario["password"], password):
        session["usuario"] = usuario["nombre"]
        session["correo"] = usuario["correo"]
        session["rol"] = usuario["rol"]

        if usuario["rol"] == "Administrador":
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("cliente"))
    else:
        flash("Correo o contraseña incorrectos", "danger")
        return redirect(url_for("inicio"))


@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():
    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip()
    telefono = request.form.get("telefono", "").strip()
    password = request.form.get("password", "")
    confirmar_password = request.form.get("confirmar_password", "")

    # Validaciones básicas del lado del servidor
    if not nombre or not correo or not telefono or not password or not confirmar_password:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for("inicio"))

    if password != confirmar_password:
        flash("Las contraseñas no coinciden.", "danger")
        return redirect(url_for("inicio"))

    if len(password) < 6:
        flash("La contraseña debe tener mínimo 6 caracteres.", "danger")
        return redirect(url_for("inicio"))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT id FROM usuarios WHERE correo=%s", (correo,))
    existente = cursor.fetchone()

    if existente:
        cursor.close()
        conexion.close()
        flash("Ese correo ya está registrado.", "danger")
        return redirect(url_for("inicio"))

    password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    sql = """
    INSERT INTO usuarios (nombre, correo, telefono, password, rol, estado)
    VALUES (%s, %s, %s, %s, 'Cliente', 'Activo')
    """
    cursor.execute(sql, (nombre, correo, telefono, password_hash))
    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Cuenta creada correctamente. Ya puede iniciar sesión.", "success")
    return redirect(url_for("inicio"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))


# ------------------------------------------------------------------
# Panel administrador
# ------------------------------------------------------------------
@app.route("/admin")
@admin_requerido
def admin():
    return render_template("admin.html")


@app.route("/admin/usuarios")
@admin_requerido
def admin_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, nombre, correo, telefono, rol, estado FROM usuarios ORDER BY id"
    )
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("usuarios.html", usuarios=usuarios)


# ------------------------------------------------------------------
# Gestión de productos (solo Administrador)
# ------------------------------------------------------------------
@app.route("/productos")
@admin_requerido
def productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("productos.html", productos=productos)


@app.route("/productos/pdf")
@admin_requerido
def productos_pdf():
    from fpdf import FPDF

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos ORDER BY codigo")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "TechStore - Listado de Productos", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(30, 8, "Código", border=1, fill=True)
    pdf.cell(80, 8, "Nombre", border=1, fill=True)
    pdf.cell(35, 8, "Precio", border=1, fill=True)
    pdf.cell(45, 8, "Categoría", border=1, fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 10)
    for producto in productos:
        pdf.cell(30, 8, str(producto["codigo"]), border=1)
        pdf.cell(80, 8, str(producto["nombre"])[:45], border=1)
        pdf.cell(35, 8, f"$ {producto['precio']:,.0f}", border=1)
        pdf.cell(45, 8, str(producto["categoria"] or ""), border=1)
        pdf.ln()

    ruta_pdf = os.path.join("/tmp", "listado_productos.pdf")
    pdf.output(ruta_pdf)

    return send_file(ruta_pdf, as_attachment=True, download_name="listado_productos.pdf")


@app.route("/registro_producto")
@admin_requerido
def registro_producto():
    return render_template("registro_producto.html")


def validar_producto(codigo, nombre, precio_raw, categoria):
    """Devuelve (es_valido, mensaje_error, precio_float)."""
    if not codigo or not nombre or not precio_raw or not categoria:
        return False, "Todos los campos son obligatorios.", None

    if not PATRON_CODIGO.match(codigo):
        return False, "El código debe tener el formato P001, P002, P003...", None

    if len(codigo) < 5:
        return False, "El código debe tener mínimo 5 caracteres.", None

    if len(nombre) < 5:
        return False, "El nombre debe tener mínimo 5 caracteres.", None

    if len(nombre) > 100:
        return False, "El nombre no debe superar los 100 caracteres.", None

    try:
        precio = float(precio_raw)
    except ValueError:
        return False, "El precio debe ser un valor numérico.", None

    if precio <= 0:
        return False, "El precio debe ser mayor que cero.", None

    if precio > 50000000:
        return False, "El precio no puede superar $50.000.000.", None

    return True, None, precio


@app.route("/guardar_producto", methods=["POST"])
@admin_requerido
def guardar_producto():
    codigo = request.form.get("codigo", "").strip()
    nombre = request.form.get("nombre", "").strip()
    precio_raw = request.form.get("precio", "").strip()
    categoria = request.form.get("categoria", "").strip()
    imagen = request.files.get("imagen")

    es_valido, error, precio = validar_producto(codigo, nombre, precio_raw, categoria)

    if not es_valido:
        flash(error, "danger")
        return redirect(url_for("registro_producto"))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT codigo FROM productos WHERE codigo=%s", (codigo,))
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        flash("Ya existe un producto con ese código.", "danger")
        return redirect(url_for("registro_producto"))

    nombre_imagen = None
    if imagen and imagen.filename:
        if archivo_permitido(imagen.filename):
            nombre_imagen = secure_filename(f"{codigo}_{imagen.filename}")
            imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_imagen))
        else:
            cursor.close()
            conexion.close()
            flash("Formato de imagen no permitido.", "danger")
            return redirect(url_for("registro_producto"))

    sql = """ INSERT INTO productos (codigo,nombre,precio,categoria,imagen)
              VALUES (%s,%s,%s,%s,%s) """
    cursor.execute(sql, (codigo, nombre, precio, categoria, nombre_imagen))
    conexion.commit()

    flash("Producto registrado correctamente", "success")

    cursor.close()
    conexion.close()

    return redirect(url_for("productos"))


@app.route("/editar_producto/<codigo>")
@admin_requerido
def editar_producto(codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    sql = "SELECT * FROM productos WHERE codigo=%s"
    cursor.execute(sql, (codigo,))
    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template("editar_producto.html", producto=producto)


@app.route("/actualizar_producto", methods=["POST"])
@admin_requerido
def actualizar_producto():
    codigo = request.form.get("codigo", "").strip()
    nombre = request.form.get("nombre", "").strip()
    precio_raw = request.form.get("precio", "").strip()
    categoria = request.form.get("categoria", "").strip()
    imagen = request.files.get("imagen")

    es_valido, error, precio = validar_producto(codigo, nombre, precio_raw, categoria)

    if not es_valido:
        flash(error, "danger")
        return redirect(url_for("editar_producto", codigo=codigo))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if imagen and imagen.filename:
        if not archivo_permitido(imagen.filename):
            cursor.close()
            conexion.close()
            flash("Formato de imagen no permitido.", "danger")
            return redirect(url_for("editar_producto", codigo=codigo))

        nombre_imagen = secure_filename(f"{codigo}_{imagen.filename}")
        imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_imagen))

        sql = """UPDATE productos SET nombre=%s, precio=%s, categoria=%s, imagen=%s
                 WHERE codigo=%s"""
        cursor.execute(sql, (nombre, precio, categoria, nombre_imagen, codigo))
    else:
        sql = """UPDATE productos SET nombre=%s, precio=%s, categoria=%s
                 WHERE codigo=%s"""
        cursor.execute(sql, (nombre, precio, categoria, codigo))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Producto actualizado correctamente", "success")

    return redirect(url_for("productos"))


@app.route("/eliminar_producto/<codigo>")
@admin_requerido
def eliminar_producto(codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    sql = "DELETE FROM productos WHERE codigo=%s"
    cursor.execute(sql, (codigo,))
    conexion.commit()

    flash("Producto eliminado correctamente", "success")

    cursor.close()
    conexion.close()

    return redirect(url_for("productos"))


# ------------------------------------------------------------------
# Dashboard cliente (solo Cliente)
# ------------------------------------------------------------------
@app.route("/cliente")
@cliente_requerido
def cliente():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (session["correo"],))
    datos_usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return render_template("cliente.html", usuario=datos_usuario)


@app.route("/cliente/actualizar", methods=["POST"])
@cliente_requerido
def cliente_actualizar():
    nombre = request.form.get("nombre", "").strip()
    telefono = request.form.get("telefono", "").strip()
    password = request.form.get("password", "").strip()

    if not nombre or not telefono:
        flash("Nombre y teléfono son obligatorios.", "danger")
        return redirect(url_for("cliente"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if password:
        if len(password) < 6:
            cursor.close()
            conexion.close()
            flash("La contraseña debe tener mínimo 6 caracteres.", "danger")
            return redirect(url_for("cliente"))

        password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        sql = "UPDATE usuarios SET nombre=%s, telefono=%s, password=%s WHERE correo=%s"
        cursor.execute(sql, (nombre, telefono, password_hash, session["correo"]))
    else:
        sql = "UPDATE usuarios SET nombre=%s, telefono=%s WHERE correo=%s"
        cursor.execute(sql, (nombre, telefono, session["correo"]))

    conexion.commit()
    cursor.close()
    conexion.close()

    session["usuario"] = nombre
    flash("Datos actualizados correctamente", "success")

    return redirect(url_for("cliente"))


if __name__ == "__main__":
    app.run(debug=True)
