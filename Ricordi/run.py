from random import randint
from flask import Flask
from flask import render_template, request, redirect, url_for
import mongobd
import next_question
from forms import LoginForm, RegisterPatientForm, SignupForm
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from time import gmtime, strftime


question = ""

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e980e0b2f255ce2e74654f35bf2a3f803227ee66'

login_manager = LoginManager(app)
login_manager.login_view = "login"

'''app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)'''


from models import Therapy, User


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


#para generar la clave secreta
#import secrets
#secrets.token_hex(20)

@app.route('/')
def index():
    return render_template("index.html")


'''@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("sign_up.html", form=form)'''

@app.route("/signup", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        type = form.type.data
        code = form.code.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email ya está siendo utilizado por otro usuario'
        else:
            if type == 'paciente':
                therapy = Therapy.get_by_code(code)
                if therapy is None:
                    error = f'No existe terapia para ese código'
                else:
                    user = User(id="",name=name, email=email,password="",type=type)
                    user.set_password(password)
                    user.save()
                    user = User.get_by_email(email)
                    if type == 'paciente' and therapy is not None:
                        therapy = Therapy(id="", therapist=therapy.therapist, patient=user.id, code=code, user="")
                        therapy.save()
                    # Dejamos al usuario logueado
                    login_user(user, True)
                    next_page = request.args.get('next', None)
                    if not next_page or url_parse(next_page).netloc != '':
                        next_page = url_for('index')
                    return redirect(next_page)
            else: 
                # Guardamos el usuario
                user = User(id="",name=name, email=email,password="",type=type)
                user.set_password(password)
                user.save()
                user = User.get_by_email(email)
                # Dejamos al usuario logueado
                login_user(user, True)
                next_page = request.args.get('next', None)
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
    return render_template("sign_up.html", form=form, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        print(user)
        if user is not None and user.check_password(form.password.data):
            login_user(user, True)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            error = f'Error al iniciar sesión'
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/chatbot') #/<int:user_id>/
@login_required
def chat():
    global question
    question = mongobd.one_random_question(current_user.id)
    time = strftime("%H:%M")
    return render_template("chatbot.html", q=question, user=current_user.name, time=time)


def chatbot_response(answer):
    global question
    mongobd.insert_answer(question, answer, current_user.id)
    nxt_question = next_question.choose_question(answer, current_user.id)
    question = nxt_question
    return nxt_question

'''
@app.route("/getRQ")
def get_random_question():
    question = mongobd.one_random_question()
    return chatbot_response(question)'''

@app.route("/get")
def get_bot_response():
    print("Holaaaaaaaaa aqui estamos")
    user_answer = request.args.get('answer')
    return chatbot_response(user_answer)

@app.route('/patients') 
@login_required
def patients():
    patients = User.get_therapists_patients(current_user.id)
    return render_template("patients.html", patients=patients)

@app.route('/patient/<int:user_id>/') 
@login_required
def patient_info(user_id):
    patient = None
    infancia = []
    adolescencia = []
    juventud = []
    etapAdulta = []
    vejez = []
    otros = []
    if (current_user.type == 'paciente' and current_user.id == user_id) or user_id in Therapy.get_patients_id(current_user.id):
        patient = mongobd.get_patients_info(user_id)
        for p in patient:
            cat = p['categorias']
            if "infancia" in cat:
                infancia.append(p)
            elif "adolescencia" in cat:
                adolescencia.append(p)
            elif "juventud" in cat:
                juventud.append(p)
            elif "etapa adulta" in cat:
                etapAdulta.append(p)
            elif "vejez" in cat:
                vejez.append(p)
            else:
                otros.append(p)
    return render_template("patient.html", p=patient, infancia=infancia, adolescencia=adolescencia, juventud=juventud, etapAdulta=etapAdulta, vejez=vejez, otros=otros)

@app.route('/new_patient', methods=['GET', 'POST']) 
@login_required
def new_patient():
    form = RegisterPatientForm()
    num = None
    if form.validate_on_submit():
        therapy = Therapy(id="", therapist=current_user.id, patient="", code=form.num.data, user=form.user.data)
        Therapy.create(therapy)
        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('patients')
        return redirect(next_page)
    else:
        num = randint(100, 999)
        while Therapy.comprobar_num(num):
            num = randint(100, 999)
        form.num.data = num
        therapies = Therapy.get_unused_codes(current_user.id)
    return render_template("new_patient.html", form=form, num=num, therapies=therapies)




# https://flask.palletsprojects.com/en/2.1.x/quickstart/
# https://j2logo.com/leccion-1-la-primera-aplicacion-flask/

# crear este fichero y luego en consola hacer (tras cd Ricordi): set FLASK_APP=run.py (CMD)        $env:FLASK_APP = "run" (Powershell)
# python -m flask run ----------- para ejecutar y servidor en localhost


# Visual chatbot:       https://buffml.com/web-based-chatbot-using-flask-api/


#pip install Flask-WTF
#pip install email-validator
#pip install flask-login
#pip install flask-sqlalchemy
#pip install cryptography

#https://parzibyte.me/blog/2021/03/29/flask-mysql-ejemplo-conexion-crud/

# Si mongodb da ECONNREFUSED 127.0.0.1:27017 -> problema de no espacio en sdxc o ir a servicios, buscar el de mongo y darle a iniciar
# https://www.youtube.com/watch?v=W0tvOEdjQ6Y
# https://bobcares.com/blog/mongodb-error-1067/