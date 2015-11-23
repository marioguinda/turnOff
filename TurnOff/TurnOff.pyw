__author__ = 'MarioGR'

from tkinter import *
from time import sleep
import tkinter.messagebox
import os
import math
import ast
import time
import re
import threading
import webbrowser

num_format = re.compile("^[1-9][0-9]*$")

def turnOffPC(event):
    result = tkinter.messagebox.askquestion("Apagar", "¿Desea apagar el ordenador?")
    if result == 'yes':
        try:
            m = "minutos"
            h = "horas"
            s = "segundos"
            
            time = entryTime.get()
            isnumber = re.match(num_format,time)
            # Checks if the entry is a number
            if not isnumber:
                tkinter.messagebox.showwarning("Error", "Introduce un numero mayor que cero!")
            # Checks if the entry is a number
            elif  is_empty(listboxTime.curselection()) :
                tkinter.messagebox.showwarning("Error", "Seleciona una medida de tiempo (h/m/s)!")
            # When seconds selected
            elif listboxTime.selection_get() == s:
                time = int(time)
                msg = os.system("shutdown -s -t " + str(time))
                if msg == 1190:
                    tkinter.messagebox.showwarning("Error", "Ya hay programado un cierre del sistema!")  
                else:
                    # Show time to turn off PC 
                    status.config(state=NORMAL)
                    counter_label(status, time)          
                    buttonTurnOff.config(relief=RAISED)
            # When minutes selected
            elif listboxTime.selection_get() == m:
                time = int(time)
                timeSecsM = time * 60
                msg = os.system("shutdown -s -t " + str(timeSecsM))     
                if msg == 1190:
                    tkinter.messagebox.showwarning("Error", "Ya hay programado un cierre del sistema!")  
                else:
                    # Show time to turn off PC 
                    status.config(state=NORMAL)
                    counter_label(status, timeSecsM)          
                    buttonTurnOff.config(relief=RAISED)
            # When hours selected        
            elif listboxTime.selection_get() == h:
                time = int(time)
                timeSecsH = time * 3600
                msg = os.system("shutdown -s -t " + str(timeSecsH))
                if msg == 1190:
                    tkinter.messagebox.showwarning("Error", "Ya hay programado un cierre del sistema!")  
                else:
                    # Show time to turn off PC 
                    status.config(state=NORMAL)
                    counter_label(status, timeSecsH)          
                    buttonTurnOff.config(relief=RAISED)
        except BaseException as e:
            print("Ecepción en una de las entradas: " + e)

def cancelTurnOffPC(event):
    result = tkinter.messagebox.askquestion("Cancelar apagado", "¿Desea cancelar el apagado del ordenador?")
    if result == 'yes':
        # Desactivate timer
        status.config(state=DISABLED)
        # Cancel shutdown
        msg = os.system("shutdown -a")
        if msg == 0:
            cancelMsg()
        #Nothing to cancel
        else:
            tkinter.messagebox.showinfo("Apagado", "El sistema no tiene ningún apagado programado.")
def cancelMsg():
     if tkinter.messagebox.showinfo("Apagado cancelado", "Se canceló el pagado del sistema."):
         root.destroy()

def printInfo():
    # AboutApplication window
    top = Toplevel(root)
    top.iconbitmap('Resources/icon256.ico')
    top.resizable(width=FALSE, height=FALSE)
    top.geometry('{}x{}'.format(460, 500))
    top.title("Sobre la aplicaci\u00F3n")

    # About label
    def openLink(link):
        webbrowser.open_new(r"http://www.ginkgosoft.es")

    textInfo="Esta aplicaci\u00F3n ha sido desarrollada por "
    textInfoLink="Ginkgosoft\u00AE."

    labelAbout = Label(top, text=textInfo, anchor=W, justify=LEFT, pady=5)
    labelAbout2 = Label(top, text=textInfoLink,fg="blue", cursor="hand2", anchor=W, justify=LEFT, pady=5)

    labelAbout.pack()
    labelAbout2.pack()
    labelAbout2.bind("<Button-1>", openLink)
    
    # Scrollbar for the license text
    scrollbar = Scrollbar(top)
    scrollbar.pack(side=RIGHT, fill=Y)

    # License text
    text = Text(top)
    licenseFile = open("gpl-3.0.txt") 
    textLicense = licenseFile.read()
    text.insert(0.0, textLicense)
    text.config(font=("Consolas", 8), state=DISABLED)
    text.pack(expand=1, fill=BOTH)

    text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text.yview)

    # Button close
    button = Button(top, text="Cerrar", command=top.destroy, width=6)
    button.pack()

def is_empty(structure):
    if structure:
        return False
    else:
        return True  

counterint = 0 
def counter_label(label, secsTurnOff):
    global counterint
    counterint = secsTurnOff
    def count():
        global counterint
        counterint = counterint - 1
        formatedTime = time.strftime("%H horas, %M minutos, %S segundos", time.gmtime(counterint))
        label.config(text="El sistema se apagará en " + formatedTime + "." + " "*70)
        label.after(1000, count)
    count()

# Main window
root = Tk(className=" Turn Off \u00AE")
root.iconbitmap('Resources/iconturnoff.ico')
root.resizable(width=FALSE, height=FALSE)
root.geometry('{}x{}'.format(400, 200))
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=5)
root.grid_columnconfigure(3, weight=2)
root.grid_rowconfigure(1, weight=2)

# Menu
menu = Menu(root)
root.config(menu=menu)

submenu = Menu(menu)
menu.add_cascade(label="Ayuda", menu=submenu)
submenu.add_command(label="Acerca de...", command=printInfo)

# Statusbar
status = Label(root, text=" "*150, bd=1, relief=SUNKEN, anchor=W)
status.grid(row=3, column=0, columnspan = 4, sticky=W)

# Labels
labelTurnOff = Label(text="Tiempo para apagado: ", borderwidth=20, anchor=W, justify=LEFT)
labelTurnOff.grid(row=0, column=0, sticky=W)

labelCancel = Label(text="Cancelar apagado: ", borderwidth=20, anchor=W, justify=LEFT)
labelCancel.grid(row=1, column=0, sticky=W)

# Entry
entryTime = Entry(text="Introduce el tiempo", borderwidth=1, width=6)
entryTime.grid(row=0, column=1, sticky=W)

# Listbox
listboxTime = Listbox(root, height=3, width=10, activestyle = DOTBOX)
listboxTime.grid(row=0, column=2)

for item in ["minutos", "segundos", "horas"]:
    listboxTime.insert(END, item)

# Buttons
imageTurnOff = PhotoImage(file="Resources/turnofficon50.png") 
imageCancel = PhotoImage(file="Resources/cancelblue50.png") 

buttonTurnOff = Button(text="Apagar", image = imageTurnOff, width=50, height=50, borderwidth=0, overrelief=RAISED)
buttonTurnOff.bind("<Button-1>", turnOffPC)
buttonTurnOff.grid(row=0, column=3, sticky=W)

buttonCancel = Button(text="Cancelar", image = imageCancel, width=50, height=50, borderwidth=0, overrelief=RAISED)
buttonCancel.bind("<Button-1>", cancelTurnOffPC)
buttonCancel.grid(row=1, column=3, sticky=W)

root.mainloop()