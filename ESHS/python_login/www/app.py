from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import random
import base64


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


# DESCOMENTAR PARA CREAR/CAMBIAR LA DB Y DESPUÉS DE UNA EJECUCIÓN VOLVER A COMENTAR
#FLAG = "flag{3ngin33ring_stud3nts_h4cking_s0ftw4r3}" #Se recomienda dejar esta flag pls
#db.create_all()
#db.session.add(User(username='admin', password='admin',email='',role='adminFalso'))
#db.session.add(User(username='su', password='qwerty',email='yonosoyCarlos@carlosMail.com',role='adminReal'))
#db.session.add(User(username='carlos', password='bien hecho', email='felicitaciones@quetengasunhermosodia.com.ar.us.xDDDD.saludosbrodarrrrrrrrr',role=f'{FLAG}'))
#db.session.commit()



@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if session.get('carlos_logged_in'):
        return render_template('indexCarlos.html')
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('index.html')
    
    
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        data = User.query.filter_by(username=name, password=passw).first()

        # Verificamos y damos informacion extra como pista
        if data and (name == "admin") and passw:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            if (name == "admin"):
                return render_template('login.html', error="Clave Incorrecta")
            else:
                return render_template('login.html', error="Usuario Incorrecto")
            


@app.route('/loginCarlos', methods=['GET', 'POST'])
def loginCarlos():
    """Login Form"""
    if request.method == 'GET':
        return render_template('loginCarlos.html')
    else:
        name = request.form['username'].lower() #user en minusculas para mas facil comparacion
        passw = request.form['password']
        data = User.query.filter_by(username=name, password=passw).first()

        # Verificamos y damos informacion extra como pista
        if data and (name == "su") and passw:
            session['carlos_logged_in'] = True
            return render_template('indexCarlos.html')
        elif name=="carlos":
            return render_template('loginCarlos.html', error="No es Carlos, Perdón.")
        elif name=="su":
            return render_template('loginCarlos.html', error="Clave incorrecta! :D")
        else:
            if 'tries' not in session:
                session['tries'] = 0
            else:
                session['tries'] += 1
            return render_template('loginCarlos.html', error=getMensajeInformativo(session['tries']))


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    session['carlos_logged_in'] = False
    return redirect(url_for('home'))

@app.route("/logoutCarlos")
def logoutCarlos():
    """Logout Form"""
    session['carlos_logged_in'] = False
    return redirect(url_for('home'))


@app.route('/infoUsuario', methods=['GET', 'POST'])
def infoUsuario():
    """ Session control"""
    if not session.get('carlos_logged_in'):
        return redirect(url_for('home'))
    #usuario logueado, le mostramos UN solo usuario
    username = request.args.get('username')
    if not username:
        return render_template('infoUsuario.html', error="No se ingresó ningún usuario")
    query = "SELECT * FROM User WHERE username = '" + username + "'"
    user = db.engine.execute(query).first()
    return render_template('infoUsuario.html', user=user)
    


    return render_template('infoUsuario.html')
    


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


def getMensajeInformativo(cantIntentos):
    app.logger.info("Cantidad de intentos: " + str(cantIntentos))
    if cantIntentos==23:
        return "Ya vas 23 intentos porfavor basta"
    if cantIntentos==24:
        return "24...."
    if cantIntentos==69:
        return "69 intentos... nice :D"
    if cantIntentos>=70000:
        return "Te dimos un diccionario para el bruteforce...... y ya deberías de saber el usuario"
    return mensajesInformativos[random.randint(0, len(mensajesInformativos) - 1)]