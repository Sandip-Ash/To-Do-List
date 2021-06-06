import tkinter as tk
from tkinter import ttk
from tkinter import *

import mysql.connector
from mysql.connector import Error

try:
    con = mysql.connector.connect(host='localhost',
                                         database='ToDoPydb',
                                         user='root',
                                         password='')#write the password if you had set during the installation else you are good to go👍😁
    if con.is_connected():
        db_Info = con.get_server_info()
        
except Error as e:
    print("Error while connecting to MySQL", e)

dicn={}
task_in=''
slno=0
# slcmd=' '

def add():
    task_in = name_entered.get()
    data = (task_in,)
    sql = 'insert into todolist values(%s);'
    c = con.cursor()
    c.execute(sql, data)
    con.commit()

def showtasks():
    c = con.cursor()
    sql = 'select * from todolist;'
    c.execute(sql)
    tasks = c.fetchall()
    for i in range(1, (len(tasks) + 1)):
        task1 = tasks[(i - 1)]

        for j in range(0, 1):
            task2 = task1[j]
            dicn.update({i: task2})


def remove():
    tno = int(name_entered.get())
    if(tno>max(dicn.keys())):
        b_label.configure(text="Please enter a valid task number")
    else:
        data = (dicn[tno],)
        sql = f'delete from todolist where title= %s;'
        c = con.cursor()
        c.execute(sql,data)
        con.commit()
        dicn.clear()
    showtasks()

win= tk.Tk()
win.geometry("500x150+500+300")
win.resizable(False,False)
win.title("Python GUI To-Do-List")



a_label=ttk.Label(win, text="Hello! Welcome to Python GUI To-Do-List")
a_label.place(x=6,y=4)

b_label=ttk.Label(win, text="Click on show tasks to activate Remove button")
b_label.place(x=16,y=40, width=350)


name=tk.StringVar()

name_entered= ttk.Entry(win, width=12, textvariable=name)

flagop = 0
func_active=""
def exitgui():
    exit()

def showtasksgui():
    global flagop

    Removebtn.configure(state="normal")
    b_label.place_forget()
    name_entered.place_forget()
    Confirmaddbtn.place_forget()

    stwin = tk.Tk()
    stwin.geometry("500x650+100+100")
    stwin.title("All Tasks")

    button2 = ttk.Button(stwin, text="REFRESH", command=showtasksgui)
    button2.pack(side=BOTTOM, pady=3)
    stList =Listbox(stwin, height=350, width=150)
    stList.pack(side=LEFT,)

    Showbtn.configure(state="disabled")
    showtasks()
    for m in dicn:
        stList.insert(m, f"{m}. {dicn[m]}")
    stwin.mainloop()




def addtasksgui():
    b_label.place(x=16,y=40, width=400)
    b_label.configure(text="Please enter the task to be added")
    name_entered.place(x=16,y=65)
    name_entered.configure(width=60)
    Confirmaddbtn.place(x=400,y=63)
    global func_active
    func_active="add"
    Showbtn.configure(state="disabled")
    Removebtn.configure(state="disabled")

def remtasksgui():
    b_label.place(x=16, y=40, width=400)
    b_label.configure(text="Please enter the task number to be removed")
    name_entered.place(x=16, y=65)
    name_entered.configure(width=20)
    Confirmaddbtn.place(x=400, y=63)
    global func_active
    func_active = "remove"
    Showbtn.configure(state="disabled")
    Removebtn.configure(state="disabled")

def check(event):
    alpha=Confirmaddbtn['text']
    if(alpha=="ADD"):
        add()
        b_label.configure(text="Task entered successfully")
        name_entered.delete(0, 'end')
    elif(alpha=="REMOVE"):
        b_label.configure(text="Task removed successfully")
        remove()
        name_entered.delete(0,'end')

    if (flagop == 1):
        Removebtn.configure(state="normal")
    else:
        Removebtn.configure(state="disabled")
    Showbtn.configure(state="normal")
    # b_label.place_forget()
    name_entered.place_forget()
    Confirmaddbtn.place_forget()
    Exitbtn.focus_set()


def on_focus_in_shwbtn(event):
    if event.widget == win:
        Showbtn.configure(state="normal")

win.bind("<FocusIn>",on_focus_in_shwbtn)

def entry_key_check(event):
    if event.widget == name_entered:
        if(func_active=="add"):
            if (name_entered.get() == ""):
                Confirmaddbtn.configure(text="CANCEL")
            elif(name_entered.get() != ""):
                Confirmaddbtn.configure(text="ADD")
        elif(func_active=="remove"):
            if (name_entered.get() == ""):
                Confirmaddbtn.configure(text="CANCEL")
            elif(name_entered.get() != ""):
                Confirmaddbtn.configure(text="REMOVE")


name_entered.bind("<KeyPress>",entry_key_check)

Exitbtn = ttk.Button(win, text='EXIT', command=exitgui)
Exitbtn.place(x=400,y=115)

Addbtn = ttk.Button(win, text='ADD TASKS', command=addtasksgui)
Addbtn.place(x=150,y=115)

Removebtn = ttk.Button(win, text='REMOVE TASKS', command=remtasksgui)
Removebtn.place(x=270,y=115)
if(flagop==1):
    Removebtn.configure(state="normal")
else:
    Removebtn.configure(state="disabled")

Showbtn = ttk.Button(win, text='SHOW TASKS', command=showtasksgui)
Showbtn.place(x=30,y=115)

Confirmaddbtn=ttk.Button(win, text="CANCEL")
Confirmaddbtn.bind('<Button-1>', check)

win.mainloop()
