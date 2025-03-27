from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedTk
import threading
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import re
import serial
from past.builtins import xrange
import math
import serial.tools.list_ports
import struct
from datetime import datetime

win=ThemedTk()
win.title("My GUI")
win.geometry('600x400')
win.resizable(True, True)

s=Style(win)
s.theme_use("arc")

def donothing():
    filewin = Toplevel(win)
    filewin.title("Resulted graph")
    button = Button(filewin, text="Do nothing button")
    button.pack()

def setting():
    filewin = Toplevel(win)
    filewin.title("Setting")
    Label(filewin, text="first option", font=('Calibri 10')).pack(padx=50,
                                                                    pady=5)
    start=Entry(filewin, width=35)
    start.pack(padx=20, pady=10)

    button = Button(filewin, text="OK")
    button.pack(padx=10, pady=10)

def About():
    aboutwin = Toplevel(win)
    aboutwin.title("About")
    Label(aboutwin, text="Sample Windows GUI", font=('Calibri 20')).pack(padx=10, pady=5)
    Label(aboutwin, text="Copyright 2024", font=('Calibri 10')).pack(padx=10, pady=5)

def Rgraph():
    global canvas, xx, yy
    graphwin = Toplevel(win)
    graphwin.title("Resulted graph")
    fig,ax = plt.subplots(figsize=(6.5, 4))
    plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
    plt.title("Diagram")
    plt.xlabel("x")
    plt.ylabel("y")
    canvas = FigureCanvasTkAgg(fig,master = graphwin)
    canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=50,pady=50)
    toolbar = NavigationToolbar2Tk(canvas, graphwin)
    toolbar.update()
    toolbar.pack(fill=BOTH, expand=True, padx=50)
    plt.plot(xx,yy)
    canvas.draw()

def generate_sample_data():  
    global xx, yy , data_to_store 
    xx = np.arange(0, 10, 0.1)  
    yy = np.sin(xx) * 2 + np.random.normal(0, 0.2, len(xx))  
    data_to_store = [f"x: {x:.2f}, y: {y:.2f}" for x, y in zip(xx, yy)]  

def Rdata():
    global mylist, scroll_bar, data_to_store
    datawin = Toplevel(win)
    datawin.title("Stored data")
    scroll_bar = Scrollbar(datawin, orient="vertical")
    mylist = Listbox(datawin, width=70, height=10, yscrollcommand = scroll_bar.set, font=("Calibri", 12))
    scroll_bar.pack( anchor = S, side = RIGHT, fill = X, pady=30)
    mylist.pack( side = BOTTOM, anchor = CENTER, fill = Y , pady=30)
    printSth(data_to_store)
   
menubar = Menu(win)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Setting", command=setting)
filemenu.add_command(label="Resulted graph", command=Rgraph)
filemenu.add_command(label="Stored data", command=Rdata)

menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)

menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=About)
menubar.add_cascade(label="Help", menu=helpmenu)

win.config(menu=menubar)

p2 = Progressbar(win, orient=HORIZONTAL, length=210, mode='indeterminate')

ports = []
for port in serial.tools.list_ports.comports():
    ports.append(port.name)
print(ports)

if (ports!=[]):
   ser = serial.Serial(ports[0], baudrate=115200, bytesize=8, timeout=2,
                    stopbits=serial.STOPBITS_ONE)
   ser.flushInput()
   ser.flushOutput()

def threading2():
    t1=threading.Thread(target=main)
    t1.start()
   
b1=Button(win, text="Start", command=threading2)
b1.pack(pady = 30)
p2.pack( pady = 10,padx=20)

label5=Label(win, text="", font=('Calibri 12'))
label5.pack(pady = 10)

def printSth(x): 
    global mylist, scroll_bar, data_to_store
    mylist.delete(0, END)  
    for item in data_to_store:  
        mylist.insert(END, item)  
    scroll_bar.config( command = mylist.yview )
    mylist.see(END)

def save_txt(line,f):
    with open(f, 'a') as output:
        output.write(line)
        output.write('\n')

def main():
    global C 
    generate_sample_data() 
    try:
      C.pack_forget()
      C = Canvas(win, height=400, width=400)
      
    except:
      C = Canvas(win, height=400, width=400)

    if (ports!=[]):
       print("serial port is connected")
       
       if (ser.isOpen() == False):
          ser.open()

       print('Done!')
       
    else:
       label5.config(text="Serial port is not connected.")
       print("Serial port is not connected.")
       label5.pack()
       
def _clear(xx,yy):
   plt.cla()
   plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
   plt.title("My Diagram")
   plt.xlabel("x")
   plt.ylabel("y")
   canvas.draw()
    
win.mainloop()

if __name__ == "__main__":
    main()

