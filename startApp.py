from tkinter import *
from tkinter import messagebox as ms
import sqlite3
import os
from subprocess import call
import sys

db = sqlite3.connect('project.db')
cur = db.cursor()

# drop_table="DROP TABLE IF EXISTS User"
# cur.execute(drop_table)

cur.execute(""" CREATE TABLE IF NOT EXISTS User (
    username text NOT NULL UNIQUE,
    password text NOT NULL,
    active INTEGER DEFAULT 0,
    id INTEGER NOT NULL PRIMARY KEY
)
""")

cur.execute("SELECT * FROM User")
x = cur.fetchall()
# print(x)
db.commit()
db.close()


class main():
    def __init__(self,master):
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.new_username = StringVar()
        self.new_password = StringVar()
        self.widgets()

    def login(self):
        db = sqlite3.connect('project.db')
        cur = db.cursor()
        active_true = """Update User set active = 0 where active=1"""
        cur.execute(active_true)
        get_user = ("SELECT * FROM User WHERE username = ? AND password = ?")
        cur.execute(get_user, [(self.username.get()),(self.password.get())])
        user_details = cur.fetchall()
 #       print(user_details)
        if user_details:
            self.show_menu()
            
        else:
            ms.showerror('Username Not Found','Please enter a valid Username.')

        db.commit()
        db.close()

    def create_new_user(self):
        db = sqlite3.connect('project.db')
        cur = db.cursor()
        active_true = """Update User set active = 0 where active=1"""
        cur.execute(active_true)
        cur.execute("SELECT username from User")
        records = cur.fetchall()
        #print(records)
        flag=0
        for r in records:
            if r[0]==self.new_username.get():
                ms.showerror("Username Taken", "Please Enter a Unique Username. ")
                flag=1
        
        if flag==0:
            add_details = 'INSERT INTO User(username,password) VALUES(?,?)'
            cur.execute(add_details, [(self.new_username.get()),(self.new_password.get())])
            ms.showinfo("Success!", "Account Created Successfully")
            self.log()
            cur.execute("SELECT *, oid from User")
            records = cur.fetchall()
            # print(records)


        db.commit()

    def widgets(self):
        self.head = Label(self.master,text = 'LOGIN',font = ('Arial',20),pady = 10)
        self.head.pack()
        self.logf = Frame(self.master,padx =10,pady = 10)
        Label(self.logf,text = 'Username: ',font = ('Arial',12),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.logf,text = 'Password: ',font = ('',12),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.logf,text = ' Login ',bd = 3 ,font = ('',12),padx=5,pady=5,command=self.login).grid()
        Button(self.logf,text = ' Create Account ',bd = 3 ,font = ('',12),padx=5,pady=5,command=self.cr).grid(row=2,column=1)
        self.logf.pack()
        
        self.crf = Frame(self.master,padx =10,pady = 10)
        Label(self.crf,text = 'Username: ',font = ('',12),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.new_username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.crf,text = 'Password: ',font = ('',12),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.new_password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.crf,text = 'Create Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.create_new_user).grid()
        Button(self.crf,text = 'Go to Login',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid(row=2,column=1)

        self.menu = Frame(self.master,padx =10,pady = 10)
        Button(self.menu,text = 'Journal',bd = 5 ,font = ('',12),padx=8,pady=3,command=self.journal).grid(row=0,column=0)
        Button(self.menu,text = 'Paint',bd = 5 ,font = ('',12),padx=8,pady=3,command=self.paint).grid(row=0,column=1)
        Button(self.menu,text = 'Notepad',bd = 5 ,font = ('',12),padx=8,pady=3,command=self.notepad).grid(row=0,column=2)

    def notepad(self):
        global root
        root.destroy()
        call(["python", "Notepad.py"])

    def paint(self):
        global root
        root.destroy()
        call(["python", "Paint.py"])

    def journal(self):
        global root
        db = sqlite3.connect('project.db')
        cur = db.cursor()
        active_true = """Update User set active = 1 where username=? AND password=?"""
        cur.execute(active_true,[(self.username.get()),(self.password.get())])
        db.commit()
        db.close()
        root.destroy()
        call(["python", "Journal.py"])

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def cr(self):
        self.new_username.set('')
        self.new_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()

    def show_menu(self):
        self.crf.pack_forget()
        self.logf.pack_forget()
        self.head['text'] = self.username.get() + '\n Logged In'
        self.menu.pack()

root = Tk()
root.geometry("400x350+350+150")
root.title("Login Form")
main(root)
root.mainloop()