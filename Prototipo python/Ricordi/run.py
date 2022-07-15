from flask import Flask
from flask import render_template, request, redirect, url_for
import mongobd
import next_question
from forms import SignupForm
from flask_login import LoginManager

question = ""

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e980e0b2f255ce2e74654f35bf2a3f803227ee66'
login_manager = LoginManager(app)

#para generar la clave secreta
#import secrets
#secrets.token_hex(20)

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/signup/", methods=["GET", "POST"])
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
    return render_template("sign_up.html", form=form)


@app.route('/chatbot/<int:user_id>/')
def chat(user_id):
    global question
    question = mongobd.one_random_question()
    return render_template("chatbot.html", user_id=user_id, q=question)


def chatbot_response(answer):
    global question
    mongobd.insert_answer(question, answer)
    nxt_question = next_question.choose_question(answer)
    question = nxt_question
    return nxt_question

'''
@app.route("/getRQ")
def get_random_question():
    question = mongobd.one_random_question()
    return chatbot_response(question)'''

@app.route("/get")
def get_bot_response():
    user_answer = request.args.get('answer')
    return chatbot_response(user_answer)



# https://flask.palletsprojects.com/en/2.1.x/quickstart/
# https://j2logo.com/leccion-1-la-primera-aplicacion-flask/

# cerar este fichero y luego en consola hacer (tras cd Ricordi): set FLASK_APP=run.py (CMD)        $env:FLASK_APP = "run" (Powershell)
# python -m flask run ----------- para ejecutar y servidor en localhost


# Visual chatbot:       https://buffml.com/web-based-chatbot-using-flask-api/


#pip install Flask-WTF
#pip install email-validator
#pip install flask-login