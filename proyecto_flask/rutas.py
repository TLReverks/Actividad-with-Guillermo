from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return '¡Hola, mundo!'

@app.route('/productos')
def productos():
    return '¡Aquí están nuestros productos!'

app.run(debug=True)