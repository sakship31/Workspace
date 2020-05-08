import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3
from tkinter import messagebox as ms
from datetime import datetime
import os
from subprocess import call

#Add, Edit, Delete Entries
#Add Images
db = sqlite3.connect('project.db')
cur = db.cursor()
#cur.execute("DROP TABLE Journal")
cur.execute(""" CREATE TABLE IF NOT EXISTS Journal (
    title text NOT NULL,
    content text NOT NULL,
    datetime text NOT NULL,
    userid INTEGER NOT NULL,
    entryid INTEGER NOT NULL PRIMARY KEY,
    FOREIGN KEY(userid) REFERENCES User(id)
)
""")

db.commit()
db.close()

class JournalApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for fr in (AddEntry,ViewEntries):
            frame1 = fr(container,self)
            self.frames [fr] = frame1
            frame1.grid(row=0, column=0, sticky = "nsew")
        self.show_frame(ViewEntries)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    

    def widgets(self):
        self.head = Label(self.master,text = 'My Journal',font = ('Arial',20),pady = 10)
        self.head.pack()



class AddEntry(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        add_label = ttk.Label(self, text = "Add Entry", font = ('Arial',20))
        add_label.pack(pady=10,padx=10)
        return_button = ttk.Button(self, text = "Go Back to My Journal", command=lambda: controller.show_frame(ViewEntries))
        return_button.pack()
        logout_button = ttk.Button(self, text = "Logout", command=self.logout)
        logout_button.pack()
        self.entry = tk.Text(self, height=18, width=55)
        self.title = StringVar()
        self.show_form()
        
    def logout(self):
        db = sqlite3.connect('project.db')
        cur = db.cursor()
        active_true = """Update User set active = 0 where active = 1"""
        cur.execute(active_true)
        db.commit()
        db.close()
        global root
        root.destroy()
        call(["python", "startApp.py"])

    def show_form(self):
        title_text = Label(self,text = "Title",)
        entry_text = Label(self,text = "Entry",)

        title_text.place(x = 15, y = 100)
        entry_text.place(x = 15, y =150)

        title_entry = Entry(self,textvariable = self.title, width = "30")
        scroll = ttk.Scrollbar(self)
        title_entry.place(x = 15, y = 120)
        self.entry.place(x = 15, y = 170)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.config(command=self.entry.yview)
        self.entry.config(yscrollcommand=scroll.set)

        add_button = ttk.Button(self, text = "Submit", command=self.add_entry)
        add_button.pack(side = BOTTOM)
        
    def add_entry(self):
        journal_entry = self.entry.get("1.0","end")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)	
        db = sqlite3.connect('project.db')
        cur = db.cursor()
        cur.execute("SELECT id FROM User WHERE active = 1 ")
        activeid = cur.fetchall()
        act = activeid[0]
        print(activeid)
        add_details = 'INSERT INTO Journal(title,content,datetime,userid) VALUES(?,?,?,?)'
        cur.execute(add_details, [(self.title.get()),(journal_entry),(dt_string),(act[0])])
        cur.execute("SELECT * from Journal")
        records = cur.fetchall()
        print(records)
        db.commit()
        db.close()
    



class ViewEntries(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        add_label = tk.Label(self, text = "Your Journal Entries", font = ('Arial',20))
        add_label.pack(pady=10,padx=10)
        add_button = tk.Button(self, text = "Add New Entry", command=lambda: controller.show_frame(AddEntry))
        add_button.pack()



root = JournalApp()
root.title("MyJournal")
root.geometry("500x500")
root.mainloop()
