import subprocess as sub
from tkinter import *
from PIL import ImageTk, Image, ImageSequence
import pyttsx3
import time
import threading as tr
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Inicialización de pyttsx3
name = "juanita"
engine = pyttsx3.init()
engine.setProperty('rate', 145)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
# Declaración de los elementos de la ventana principal
main_window = Tk()
main_window.title("Juanita AI")
main_window.geometry("800x480")
main_window.configure(bg="#0082c8")
main_window.resizable(0, 0)

juanita_gif_path = "Images/juanita.gif"
info_gif = Image.open(juanita_gif_path)
gif_nframes = info_gif.n_frames

# Label del título y foto de Juanita
label_name = Label(main_window, text="Juanita AI", fg="#203A43", bg="#36D1DC",
                   font=('Arial', 35, 'bold')).pack(pady=10)
juanita_gif_list = [PhotoImage(file=juanita_gif_path, format=f'gif -index {i}') for i in range(gif_nframes)]
label_gif = Label(main_window)
label_gif.pack()

def animate_gif(index):
    frame = juanita_gif_list[index]
    index += 1
    if index == gif_nframes:
        index = 0
    label_gif.configure(image=frame)
    main_window.after(50, animate_gif, index)

animate_gif(0)

# Canvas en dónde se ubicarán los comandos
canvas = Canvas(bg="#0575E6", height=480, width=200)
canvas.place(x=0, y=0)
# Texto en dónde se mostrará información de Wikipedia
text_info = Text(main_window, bg="#0575E6", fg="white")
text_info.place(x=0, y=250, height=350, width=200)
# Función de hablar


def talk(text):
    time.sleep(0.5)
    engine.say(text)
    engine.runAndWait()
    text_info.delete('1.0', 'end')
    if engine._inLoop:
        engine.endLoop()

# Ventana en donde se pide el nombre del usuario
def give_name():
    global name_entry
    name_window = Toplevel()
    name_window.title("¿Cómo te llamas?")
    name_window.geometry('350x100')
    name_window.configure(bg="#434343")
    name_window.resizable(0, 0)
    title_label = Label(name_window, text="¿Cómo te llamas?", fg="white",
                        bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    name_entry = Entry(name_window, width=25)
    name_entry.pack(pady=1)
    button_save = Button(name_window, text="Guardar", bg='#16222A',
                         fg="white", width=8, height=1, command=save_name).pack(pady=2)


def thread_give_name():
    t = tr.Thread(target=give_name)
    t.start()
# Función para guardar el nombre en una archivo txt


def save_name():
    name_user = name_entry.get()
    talk(f"Bienvenido {name_user}!")
    try:
        with open("nombre.txt", 'w') as f:
            f.write(name_user)
    except FileNotFoundError as e:
        file = open("nombre.txt", 'w')
        file.write(name_user)
# Función en donde Juanita saluda al usuario


def say_hello():
    try:
        with open("nombre.txt") as f:
            for name in f:
                talk(f"Hola {name}, bienvenido!")
    except FileNotFoundError as e:
        talk("Hola, ¿cómo te llamas?")
# Función que saluda con hilos


def thread_hello():
    t = tr.Thread(target=say_hello)
    t.start()
# Función que verifica si el usuario ha guardado su nombre


def check_name_window():
    try:
        with open("nombre.txt") as f:
            pass
    except FileNotFoundError as e:
        thread_give_name()


# Invocación de la ventana del nombre y el saludo
check_name_window()
thread_hello()


def read_talk():
    text = text_info.get("1.0", "end")
    talk(text)


def write_text(textc):
    text_info.insert(INSERT, textc)




def run_juanita():
    chat = ChatBot("juanita", database_uri=None)
    trainer = ListTrainer(chat)
    conver = [
        "Buenos días",
        "Hola",
        "¿cómo te llamas?",
        "Me llamo Juanita",
        "¿Cómo te encuentras hoy?",
        "Bien",
        "Eso es muy buena señal.",
        "¿Cómo te encuentras hoy?",
        "Mal",
        "Lo siento mucho."
    ]
    trainer.train(conver)
    trainer.train("chatterbot.corpus.spanish")
    #talk("Vamos a conversar...")  
    while True:
        var = input()                                                        
        print("Tú:", var)
        answer = chat.get_response(var)
        print("Juanita:", answer)
        talk(answer)
        if 'adios' in var.split():
            break      
            
    main_window.update()

tr.Thread(target=run_juanita).start()



# Ventanas para agregar cosas


def open_file_window():
    global namef_entry, rutef_entry
    file_win = Toplevel()
    file_win.title("Agregar archivos")
    file_win.geometry('300x200')
    file_win.configure(bg="#434343")
    file_win.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(file_win)} center')
    title_label = Label(file_win, text="Agrega un archivo", fg="white",
                        bg="#434343", font=('Arial', 15, 'bold')).pack(pady=3)
    text_name = Label(file_win, text="Nombre del archivo", fg="white",
                      bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    namef_entry = Entry(file_win)
    namef_entry.pack(pady=1)
    text_rute = Label(file_win, text="Ruta del archivo", fg="white",
                      bg="#434343", font=('Arial', 10, 'bold')).pack(pady=2)
    rutef_entry = Entry(file_win, width=30)
    rutef_entry.pack(pady=1)
    #button_add = Button(file_win, text="Agregar", bg='#16222A', fg="white", width=8, height=1, command=add_files).pack(pady=5)




# Botones main_window


button_speak = Button(main_window, text="Hablar", bg='#b6fbff', fg="black", font=('Arial', 10, 'bold'), command=read_talk) \
    .place(x=645, y=195, height=30, width=100)


# Ejecución de mainloop()
main_window.mainloop()