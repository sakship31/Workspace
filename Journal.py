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


#Add, Edit, Delete Entries
#Add Images
db = sqlite3.connect('project.db')
cur = db.cursor()
# cur.execute("DROP TABLE Journal")
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
        global root
        root.destroy()
        call(["python", "Journal.py"])
       # controller.show_frame(ViewEntries)
    



class ViewEntries(tk.Frame):
    # list1=[]
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

        # delete_entry_btn=ttk.Button(change_label,width=10,text="Delete")
        # delete_entry_btn.grid(row=0,column=2,padx=2)

        logout_btn=ttk.Button(change_label,width=10,text="Log Out",command=self.logout)
        logout_btn.grid(row=0,column=3,padx=2)

        space=ttk.Label(self,text="",background="white")

        scroll_bar=tk.Scrollbar(self)
        list_box=tk.Listbox(self)
        scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
        list_box.pack(fill=tk.BOTH,expand=True)
        scroll_bar.config(command=list_box.yview)
        list_box.config(yscrollcommand=scroll_bar.set)
        list1=[]
        db = sqlite3.connect('project.db')
        cur = db.cursor()
        cur.execute("SELECT id FROM User WHERE active = 1 ")
        activeid = cur.fetchall()
        act = activeid[0]
        # print(activeid)
        # print(act)
        get_title=("SELECT title,content,datetime FROM Journal WHERE userid = ? ")
        cur.execute(get_title,act)
        titles=cur.fetchall()
        i=0
        print(titles)
        for title1 in titles:
            list1.append(title1[0])
            list1.append(title1[1])
            list1.append(title1[2])
            i+=1
 #      print(list1)
        cur.execute("SELECT * from Journal")
        records = cur.fetchall()
        print(records)
        self.update_view(list1,list_box)
        cur.execute("SELECT * from Journal")
        print("should print journal")
        records = cur.fetchall()
        print(records)
        db.commit()
        db.close()
        print("heyy")
        delete_entry_btn=ttk.Button(change_label,width=10,text="Delete",command=lambda: self.delete(list_box,list1))
        delete_entry_btn.grid(row=0,column=2,padx=2)

    def update_view(self,list1,list_box):
        for entry in list1:
            list_box.insert("end",entry)

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
#        pass
        del_title_index=list_box.curselection()
        # del_title=int(del_title)
        print("sjdsjdsjdhsjh")
        print(del_title_index)
        del_title=list1[del_title_index[0]]
        print(del_title)
        tup1=()
        tup2=()
        tup1=tup1+(del_title_index[0]+1,)
        tup2=tup2+((del_title_index[0]+2),) 
        print(tup1)
        print(tup2)
        print(len(del_title))
        print(len((del_title,)))
        if del_title_index:
            list_box.delete(tup2)
            list_box.delete(tup1)
            list_box.delete(del_title_index)            
            db = sqlite3.connect('project.db')
            cur = db.cursor()
            cur.execute("SELECT id FROM User WHERE active = 1 ")
            activeid = cur.fetchall()
            act = activeid[0]
            del_entry=("DELETE FROM Journal WHERE title=?")
            cur.execute(del_entry,(del_title,))
            db.commit()
            db.close()


    def update(self, list_box,list1):
        upd_title_index=list_box.curselection()
        upd_title=list1[upd_title_index[0]]
        print(upd_title)
        db = sqlite3.connect('project.db')
        cur = db.cursor()
        upd_entry=("SELECT * FROM Journal WHERE title=?")
        cur.execute(upd_entry,(upd_title,))
        entries = cur.fetchall()
        print(entries)
        entry_list = entries[0]
        #create separate dialog box
        
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
        print(title_data, entry_data)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        add_details = 'UPDATE Journal set title=?,content=?,datetime=?,userid=? WHERE entryid = ?'
        cur.execute(add_details, [(title_data),(entry_data),(dt_string),(self.entry_list[3]),(self.entry_list[4])])
        cur.execute("SELECT * from Journal")
        records = cur.fetchall()
        print(records)
        db.commit()
        db.close()
        #print(self.entry_list)
        self.top.destroy()

def onClick(entry_list):
    inputDialog = MyDialog(root,entry_list)
    root.wait_window(inputDialog.top)
    #print(entry_list)


root = JournalApp()
#username = 'Empty'
#mainButton = tk.Button(root, text='Click me', command=onClick)
#mainButton.pack()
root.title("Journal")
root.geometry("500x500")
root.mainloop()
