import PySimpleGUI as gui

layout = [[gui.Text("App de terapia ocupacional para pacientes con demencia")], [gui.Button("OK")]]

window = gui.Window("Demo", layout)

while True:
    event, values = window.read()
    if event == "OK" or event == gui.WIN_CLOSED:
        break

window.close()