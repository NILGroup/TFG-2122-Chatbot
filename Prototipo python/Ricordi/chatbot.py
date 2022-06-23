import sys
import time
from pip import main
import pyttsx3
from tkinter import *
from tkinter import ttk
import mongobd
import next_question
import window




engine = pyttsx3.init()
engine.setProperty('rate', 145)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Declaración de los elementos de la ventana principal
main_window = Tk()
main_window.title("RICORDA")
main_window.geometry("800x560")
main_window.configure(bg="#ede8df")
main_window.resizable(0, 0)

text_entry = ttk.Entry()
text_entry.place(x=280, y=400, width=200)

label_name = Label(main_window, text="RICORDA", font=('Arial', 35, 'bold')).pack(pady=10)



window.layout(main_window)

#main_window.mainloop()


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
    mongobd.insert_answer(question, answer)
    if 'adios' in answer.split():
        break
    question = next_question.choose_question(answer)

print("No hay más preguntas")
sys.exit()
        



