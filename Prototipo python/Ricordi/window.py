from tkinter import *

def layout(main_window):
    
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