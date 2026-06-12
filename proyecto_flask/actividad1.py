from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return 'Bienvenido a mi sitio web'

@app.route('/saludo')
def saludo():
    return "Hola aprendiz ADSO"

@app.route('/inventario')
def inventario():
    return "sistema de inventario activo"

@app.route('/usuarios')
def usuarios():
    return "sistema usuarios activo"

app.run(debug=True)