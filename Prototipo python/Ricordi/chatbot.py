import sys
import time
from pip import main
import pyttsx3
import mongobd
import next_question




engine = pyttsx3.init()
engine.setProperty('rate', 145)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(text):
    time.sleep(0.5)
    engine.say(text)
    engine.runAndWait()
    if engine._inLoop:
        engine.endLoop()



talk("Hola, empecemos")
question = mongobd.one_random_question()

while question:
    '''questions = mongobd.one_question()
    for question in questions:
        print("Juanita:", question)
        talk(question)
        var = input()
        print("Tú:", var)
        mongobd.insert_answer(question, var)
        if 'adios' in var.split():
            break'''
    
    print("Juanita:", question)
    talk(question)
    answer = input()
    print("Tú:", answer)
    if 'adios' in answer.split():
        break
    mongobd.insert_answer(question, answer)
    question = next_question.choose_question(answer)

print("No hay más preguntas")
sys.exit()
        

