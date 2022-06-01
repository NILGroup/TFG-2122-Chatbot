import time
from pip import main
import pyttsx3
from tkinter import *
from tkinter import ttk
import mongobd




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


def talk(text):
    time.sleep(0.5)
    engine.say(text)
    engine.runAndWait()
    if engine._inLoop:
        engine.endLoop()



talk("Vamos a conversar")
while True:
    questions = mongobd.query()
    for question in questions:
        print("Juanita:", question)
        talk(question)
        var = input()                                                        
        print("Tú:", var)
        mongobd.insert(question, var)
        if 'adios' in var.split():
            break
        

def layout():

    # to show chat window
    main_window.deiconify()
    main_window.title("CHATROOM")
    main_window.resizable(width = False,
                            height = False)
    main_window.configure(width = 470,
                            height = 550,
                            bg = "#17202A")
    
    line = Label(main_window,
                        width = 450,
                        bg = "#ABB2B9")
        
    line.place(relwidth = 1,
                    rely = 0.07,
                    relheight = 0.012)
        
    textCons = Text(main_window,
                            width = 20,
                            height = 2,
                            bg = "#17202A",
                            fg = "#EAECEE",
                            font = "Helvetica 14",
                            padx = 5,
                            pady = 5)
        
    textCons.place(relheight = 0.745,
                        relwidth = 1,
                        rely = 0.08)
        
    labelBottom = Label(main_window,
                                bg = "#ABB2B9",
                                height = 80)
        
    labelBottom.place(relwidth = 1,
                            rely = 0.825)
        
    entryMsg = Entry(labelBottom,
                            bg = "#2C3E50",
                            fg = "#EAECEE",
                            font = "Helvetica 13")
        
    # place the given widget
    # into the gui window
    entryMsg.place(relwidth = 0.74,
                        relheight = 0.06,
                        rely = 0.008,
                        relx = 0.011)
        
    entryMsg.focus()
        
    # create a Send Button
    buttonMsg = Button(labelBottom,
                            text = "Send",
                            font = "Helvetica 10 bold",
                            width = 20,
                            bg = "#ABB2B9")
                            #command = lambda : sendButton(entryMsg.get()))
        
    buttonMsg.place(relx = 0.77,
                            rely = 0.008,
                            relheight = 0.06,
                            relwidth = 0.22)
        
    textCons.config(cursor = "arrow")
        
    # create a scroll bar
    scrollbar = Scrollbar(textCons)
        
    # place the scroll bar
    # into the gui window
    scrollbar.place(relheight = 1, relx = 0.974)
        
    scrollbar.config(command = textCons.yview)
        
    textCons.config(state = DISABLED)

layout()

main_window.mainloop()