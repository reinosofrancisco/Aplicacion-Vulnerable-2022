from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import random
import base64
import hashlib
from passlib.hash import pbkdf2_sha256

import requests
import json




app = Flask(__name__)
app.secret_key = "muy secreta"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

cantIncorrectos = 0
mensajesInformativos = ["Uno pensaria que estos comentarios sirven para algo", 
"Probaste admin/admin ya?",
"Proba de nuevo, seguro funciona", 
"El bicho te manda saludos suuuu",
"Leer mensajes de errores no parece el mejor uso de tu tiempo",
"Por las dudas, probaste apagando y volviendo a prender?",
"Y si la flag son lxs amigxs que hicimos en el camino?",
"El grupo ESHS les manda saludos!",
"Esta su es una pista, lo juro. Prestá atención a lo que te estoy diciendo.",
"Okey... Una pista: https://www.youtube.com/watch?v=dQw4w9WgXcQ",
"No podes usar Hydra, pero ya sabes que solo hay 100 opciones, no?"
] 


class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    role = db.Column(db.String(80))

    def __init__(self, username, password,email,role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.username


def add_user(username, password, email, role):
    #La owasp recomienda >310,000 para sha-256
    db.session.add(User(username=username, password=pbkdf2_sha256.using(rounds=500000, salt_size=10).hash(password), email=email, role=role))


# DESCOMENTAR PARA CREAR/CAMBIAR LA DB Y DESPUÉS DE UNA EJECUCIÓN VOLVER A COMENTAR
#FLAG = "flag{3ngin33ring_stud3nts_h4cking_s0ftw4r3}" #Se recomienda dejar esta flag pls
#db.create_all()
#add_user('admin', 'admin','admin@admin.com','adminFalso') #NO RECOMENDAMOS UN USUARIO CON CREDENCIALES BIEN CONOCIDAS Y PSSWD debil
#add_user('su','qwerty','yonosoyCarlos@carlosMail.com','adminReal') #NO RECOMENDAMOS UN USUARIO CON CREDENCIALES BIEN CONOCIDAS Y PSSWD debil
#add_user('carlos', 'bien hecho','felicitaciones@quetengasunhermosodia.com.ar.us.xDDDD.saludosbrodarrrrrrrrr','{FLAG}')
#db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        captcha_token = request.form['g-recaptcha-response']
        urlGoogle = "https://www.google.com/recaptcha/api/siteverify" #TODO: esto puede refactorizarse a una constante o en un archivo de configuración
        secret_key = "6LcEx6UgAAAAABrXLXhPHe6A576PW2axCD4uO1jX" #TODO: Mover esto a un archivo como la otra clave
        captchaData = {"secret": secret_key, "response": captcha_token}
        response = requests.post(url=urlGoogle, data=captchaData)
        responseJson = json.loads(response.text)
        data = User.query.filter_by(username=name).first()
        if data and name and passw and responseJson['success'] == True and pbkdf2_sha256.verify(passw, data.password):
            session['logged_in'] = True
            session['username'] = data.username   #esto es para mostrar la info del usuario
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Usuario o Contraseña Incorrectos")
            


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))



@app.route('/infoUsuario', methods=['GET', 'POST'])
def infoUsuario():
    """ Session control"""
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    #usuario logueado, le mostramos solo info de SU usuario (manejamos a nivel sesión esto)
    if not session['username']:
        return render_template('infoUsuario.html', error="Esto no debería de estar pasando...")
    user = User.query.filter_by(username = session['username']).first()
    return render_template('infoUsuario.html', users=user)    


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
