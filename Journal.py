import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3
from tkinter import messagebox as ms
from datetime import datetime
import os
from subprocess import call
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT
from tkinter.ttk import Frame, Label, Entry, Button


db = sqlite3.connect('project.db')
cur = db.cursor()

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
        db = sqlite3.connect('project.db')
        cur = db.cursor()
        cur.execute("SELECT id FROM User WHERE active = 1 ")
        activeid = cur.fetchall()
        act = activeid[0]
        add_details = 'INSERT INTO Journal(title,content,datetime,userid) VALUES(?,?,?,?)'
        cur.execute(add_details, [(self.title.get()),(journal_entry),(dt_string),(act[0])])
        cur.execute("SELECT * from Journal")
        records = cur.fetchall()
        db.commit()
        db.close()
        global root
        root.destroy()
        call(["python", "Journal.py"])
       
    



class ViewEntries(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        add_label = tk.Label(self, text = "Your Journal Entries", font = ('Arial',10))
        add_label.pack(pady=10,padx=10)

        change_label=ttk.Label(self)
        change_label.pack(side=tk.TOP,fill=tk.X)

        add_entry_btn=ttk.Button(change_label,width=10,text="Add",command=lambda: controller.show_frame(AddEntry))
        add_entry_btn.grid(row=0,column=0,padx=2)

        edit_entry_btn=ttk.Button(change_label,width=10,text="Edit", command=lambda: self.update(list_box,list1))
        edit_entry_btn.grid(row=0,column=1,padx=2)

        np_btn=ttk.Button(change_label,width=13,text="Go to Notepad",command=self.get_notepad)
        np_btn.grid(row=0,column=3,padx=2)

        paint_btn=ttk.Button(change_label,width=10,text="Go to Paint",command=self.get_paint)
        paint_btn.grid(row=0,column=4,padx=2)

        logout_btn=ttk.Button(change_label,width=10,text="Log Out",command=self.logout)
        logout_btn.grid(row=0,column=5,padx=2)

        space=ttk.Label(self,text="",background="white")

        scroll_bary=tk.Scrollbar(self)
        scroll_barx=tk.Scrollbar(self,orient="horizontal")
        list_box=tk.Listbox(self)
        list_box.config(yscrollcommand=scroll_bary.set)
        list_box.config(xscrollcommand=scroll_barx.set)
        scroll_bary.config(command=list_box.yview)
        scroll_barx.config(command=list_box.xview)
        scroll_bary.pack(side=tk.RIGHT,fill=tk.Y)
        list_box.pack(fill=tk.BOTH,expand=True)
        scroll_barx.pack(side=tk.BOTTOM,fill=tk.X)
        # list_box.pack(fill=tk.BOTH,side=tk.LEFT)

        list1=[]
        db = sqlite3.connect('project.db')
        cur = db.cursor()
        cur.execute("SELECT id FROM User WHERE active = 1 ")
        activeid = cur.fetchall()
        act = activeid[0]
        
        get_title=("SELECT entryid,title,content,datetime FROM Journal WHERE userid = ? ")
        cur.execute(get_title,act)
        titles=cur.fetchall()
        for title1 in titles:
            list2=[]
            for i in range(4):
                list2.append(title1[0])
                list2.append(title1[1])
                list2.append(title1[2])
                list2.append(title1[3])
            list1.append(list2)

 
        cur.execute("SELECT * from Journal")
        records = cur.fetchall()
        self.update_view(list1,list_box)
        cur.execute("SELECT * from Journal")
        records = cur.fetchall()
        db.commit()
        db.close()
        delete_entry_btn=ttk.Button(change_label,width=10,text="Delete",command=lambda: self.delete(list_box,list1))
        delete_entry_btn.grid(row=0,column=2,padx=2)

    def update_view(self,list1,list_box):
        i=1
        for entry in list1:
            x="Entry "+str(i)
            list_box.insert("end",x)
            list_box.insert("end",entry[1])
            list_box.insert("end",entry[2])
            list_box.insert("end",entry[3]) 
            i+=1           


    def get_notepad(self):
        global root
        root.destroy()
        call(["python", "Notepad.py"])

    def get_paint(self):
        global root
        root.destroy()
        call(["python", "Paint.py"])

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

    def delete(self,list_box,list1):

        del_title_index=list_box.curselection()
        if ((del_title_index[0]%4)==0):
            del_title_index1=int(del_title_index[0]/4)
            del_title=list1[del_title_index1][0]
            tup1=()
            tup2=()
            tup3=()
            tup1=tup1+(del_title_index[0]+1,)
            tup2=tup2+((del_title_index[0]+2),)
            tup3=tup3+((del_title_index[0]+3),) 
            if del_title_index:
                list_box.delete(tup3)
                list_box.delete(tup2)
                list_box.delete(tup1)
                list_box.delete(del_title_index)            
                db = sqlite3.connect('project.db')
                cur = db.cursor()
                cur.execute("SELECT id FROM User WHERE active = 1 ")
                activeid = cur.fetchall()
                act = activeid[0]
                del_entry=("DELETE FROM Journal WHERE entryid=?")
                cur.execute(del_entry,(del_title,))
                db.commit()
                db.close()


    def update(self, list_box,list1):
        upd_title_index=list_box.curselection()
        if((upd_title_index[0]%4)==0):
            upd_title_index1=int(upd_title_index[0]/4)
            upd_title=list1[upd_title_index1][0]
            db = sqlite3.connect('project.db')
            cur = db.cursor()
            upd_entry=("SELECT * FROM Journal WHERE entryid=?")
            cur.execute(upd_entry,(upd_title, ))
            entries = cur.fetchall()
            entry_list = entries[0]
            db.commit()
            db.close()
            onClick(entry_list)
            global root
            root.destroy()
            call(["python", "Journal.py"])
    

class MyDialog:
    def __init__(self, parent, entry_list):
        top = self.top = tk.Toplevel(parent)
        self.entry_list = entry_list
        add_label = tk.Label(top, text = "Edit Entry", font = ('Arial',16))
        add_label.pack(pady=10,padx=10)
    
        self.myLabel = tk.Label(top, text='Title: ')
        self.myLabel.pack()

        self.title = tk.Text(top, height=1, width=55)
        self.title.insert(END,entry_list[0])
        self.title.pack()

        self.myLabel = tk.Label(top, text='Entry: ')
        self.myLabel.pack()

        self.entry = tk.Text(top, height=18, width=55)
        self.entry.insert(END,entry_list[1])
        scroll = ttk.Scrollbar(top)
        self.entry.place(x = 15, y = 170)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.config(command=self.entry.yview)
        self.entry.config(yscrollcommand=scroll.set)
        self.entry.pack()
        self.mySubmitButton = tk.Button(top, text='Submit', command=self.edit_data)
        self.mySubmitButton.pack()

    def edit_data(self):
        db = sqlite3.connect('project.db')
        cur = db.cursor()
        title_data = self.title.get("1.0","end")
        entry_data = self.entry.get("1.0","end")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        add_details = 'UPDATE Journal set title=?,content=?,datetime=?,userid=? WHERE entryid = ?'
        cur.execute(add_details, [(title_data),(entry_data),(dt_string),(self.entry_list[3]),(self.entry_list[4])])
        cur.execute("SELECT * from Journal")
        records = cur.fetchall()
        db.commit()
        db.close()
        self.top.destroy()

def onClick(entry_list):
    inputDialog = MyDialog(root,entry_list)
    root.wait_window(inputDialog.top)


root = JournalApp()
root.title("Journal")
root.geometry("500x500")
root.mainloop()