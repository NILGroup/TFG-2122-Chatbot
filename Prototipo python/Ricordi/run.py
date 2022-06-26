from flask import Flask
from flask import render_template, request, redirect, url_for
import mongobd
import next_question

question = ""

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("sign_up.html")


@app.route('/chatbot/<int:user_id>/')
def chat():
    global question
    question = mongobd.one_random_question()
    return render_template("chatbot.html", user_id=3, q=question)


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

# cerar este fichero y luego en consola hacer: set FLASK_APP=run.py
# python -m flask run ----------- para ejecutar y servidor en localhost


# Visual chatbot:       https://buffml.com/web-based-chatbot-using-flask-api/