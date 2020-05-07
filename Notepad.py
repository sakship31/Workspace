import tkinter as tk
from tkinter import ttk
from tkinter import font,colorchooser,filedialog,messagebox
from tkinter.filedialog import askopenfile,asksaveasfilename
import os
from tkinter import simpledialog
#For Encryption/Decryption
from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import sqlite3
#--
main_app=tk.Tk()
main_app.geometry("600x600")
main_app.title("Notepad")

main_menu=tk.Menu()
main_app.config(menu=main_menu)

filemenu = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="File",menu=filemenu)

edit_menu = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="Edit",menu=edit_menu)

view_menu = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="View",menu=view_menu)

show_toolbar=tk.BooleanVar()
show_toolbar.set(True)

show_status_bar=tk.BooleanVar()
show_status_bar.set(True)

def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        tool_bar_label.pack_forget()
        show_toolbar=False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar_label.pack(side=tk.TOP,fill=tk.X)
        text_editor.pack(fill=tk.BOTH,expand=True)
        status_bar.pack(side=tk.BOTTOM)
        show_toolbar=True

def hide_status_bar():
    global show_status_bar
    if show_status_bar:
        status_bar.pack_forget()
        show_status_bar=False
    else:
        status_bar.pack(side=tk.BOTTOM)
        show_status_bar=True

view_menu.add_checkbutton(label="Tool Bar",offvalue=0,compound=tk.LEFT,variable=show_toolbar,command=hide_toolbar)
view_menu.add_checkbutton(label="Status Bar",offvalue=0,compound=tk.LEFT,variable=show_status_bar,command=hide_status_bar)

theme_menu = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="Theme",menu=theme_menu)

color_dict={
    'Light Default':('#000000','#ffffff'),
    'Dark':('#c4c4c4','#2d2d2d')
}

def change_theme_dark():
    color_combo=color_dict.get('Dark')
    fg_C,bg_C=color_combo[0],color_combo[1]
    text_editor.config(background=bg_C,fg=fg_C)

def change_theme_light():
    color_combo=color_dict.get('Light Default')
    fg_C,bg_C=color_combo[0],color_combo[1]
    text_editor.config(background=bg_C,fg=fg_C)

theme_menu.add_radiobutton(label="Light (Default)",compound=tk.LEFT,command=change_theme_light)
theme_menu.add_radiobutton(label="Dark",compound=tk.LEFT,command=change_theme_dark)


tool_bar_label=ttk.Label(main_app)
tool_bar_label.pack(side=tk.TOP,fill=tk.X)

font_tuple=tk.font.families()
font_family=tk.StringVar()
font_box=ttk.Combobox(tool_bar_label,width=30,textvariable=font_family,state="readonly")
font_box["values"]=font_tuple
font_box.current(font_tuple.index("Arial"))
font_box.grid(row=0,column=0,padx=5,pady=5)

#size

size_variable=tk.IntVar()
font_size=ttk.Combobox(tool_bar_label,width=20,textvariable=size_variable,state="readonly")
font_size["values"]=tuple(range(8,100,2))
font_size.current(4)
font_size.grid(row=0,column=1,padx=3,pady=5)

bold_btn=ttk.Button(tool_bar_label,width=3,text="B")
bold_btn.grid(row=0,column=2,padx=2)

italic_btn=ttk.Button(tool_bar_label,width=3,text="I")
italic_btn.grid(row=0,column=3,padx=2)

underline_btn=ttk.Button(tool_bar_label,width=3,text="U")
underline_btn.grid(row=0,column=4,padx=2)

font_color_btn=ttk.Button(tool_bar_label,width=3,text="A")
font_color_btn.grid(row=0,column=5,padx=2)

left_btn=ttk.Button(tool_bar_label,width=3,text="L")
left_btn.grid(row=0,column=6,padx=2)

center_btn=ttk.Button(tool_bar_label,width=3,text="C")
center_btn.grid(row=0,column=7,padx=2)

right_btn=ttk.Button(tool_bar_label,width=3,text="R")
right_btn.grid(row=0,column=8,padx=2)

scroll_bar=tk.Scrollbar(main_app)
text_editor=tk.Text(main_app)
text_editor.config(wrap="word",relief=tk.FLAT)
scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
text_editor.pack(fill=tk.BOTH,expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)
text_editor.focus_set()

text_url=''

def new_file():
    global text_url
    text_url=''
    text_editor.delete(1.0,tk.END)

def open_file():
    global text_url
    text_editor.delete("1.0",tk.END)
    text_url=askopenfile(initialdir="/",title="Open File",filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if text_url is not None:
        text=text_url.read()
        text_editor.insert("1.0",text)

# def save_file():
#     global text_url
#     try:
#         if text_url:
#             text_area_text = text_editor.get('1.0', 'end-1c')
#             save_text = open(text_url, 'w')
#             save_text.write(text_area_text)
#             save_text.close()
#         else:
#             notepad_text=text_editor.get("1.0","end-1c")
#             file=asksaveasfilename(title="Save",filetypes=[('text files','*.txt')],defaultextension = [('text files','*.txt')])
#             with open(file,"w") as content:
#                 content.write(notepad_text)
#     except:
#         return

def save_file():
    notepad_text=text_editor.get("1.0","end-1c")
    file=asksaveasfilename(title="Save",filetypes=[('text files','*.txt')],defaultextension = [('text files','*.txt')])
    with open(file,"w") as data:
        data.write(notepad_text)


filemenu.add_command(label="New",compound=tk.LEFT,command=new_file)
filemenu.add_command(label="Open",compound=tk.LEFT,command=open_file)
filemenu.add_command(label="Save",compound=tk.LEFT,command=save_file)
#filemenu.add_command(label="Save as",compound=tk.LEFT,command=saveas_file,accelerator="Ctrl+Alt+s")
filemenu.add_command(label="Exit",compound=tk.LEFT,command=main_app.destroy)

edit_menu.add_command(label="Copy",compound=tk.LEFT,command=lambda:text_editor.event_generate("<Control c>"))
edit_menu.add_command(label="Paste",compound=tk.LEFT,command=lambda:text_editor.event_generate("<Control v>"))
edit_menu.add_command(label="Cut",compound=tk.LEFT,command=lambda:text_editor.event_generate("<Control x>"))
edit_menu.add_command(label="Clear",compound=tk.LEFT,command=lambda:text_editor.delete(1.0,tk.END))

def find_func(event= None):

    def find():
        word=input_find.get()
        text_editor.tag_remove("match","1.0",tk.END)
        matches=0
        if word:
            start_pos="1.0"
            while True:
                start_pos=text_editor.search(word,start_pos,stopindex=tk.END)
                if not start_pos:
                    break
                end_pos=f"{start_pos}+{len(word)}c"
                text_editor.tag_add("match",start_pos,end_pos)
                matches+=1
                start_pos=end_pos
                text_editor.tag_config('match',foreground="red",background="yellow")

    def replace():
        word=input_find.get()
        replace_text=input_replace.get()
        content=text_editor.get(1.0,tk.END)
        new_content=content.replace(word,replace_text)
        text_editor.delete(1.0,tk.END)
        text_editor.insert(1.0,new_content)

    find_popup=tk.Toplevel()
    find_popup.geometry("450x200")
    find_popup.title("Find Word")
    find_popup.resizable(0,0)

    find_frame=ttk.LabelFrame(find_popup,text="Find and Replace word")
    find_frame.pack(pady=20)

    text_find=ttk.Label(find_frame,text="Find")
    text_replace=ttk.Label(find_frame,text="Replace")

    input_find=ttk.Entry(find_frame,width=30)
    input_replace=ttk.Entry(find_frame,width=30)

    button_find=ttk.Button(find_frame,text="Find",command=find)
    button_replace=ttk.Button(find_frame,text="Replace",command=replace)

    text_find.grid(row=0,column=0,padx=4,pady=4)
    text_replace.grid(row=1,column=0,padx=4,pady=4)

    input_find.grid(row=0,column=1,padx=4,pady=4)
    input_replace.grid(row=1,column=1,padx=4,pady=4)

    button_find.grid(row=2,column=0,padx=4,pady=4)
    button_replace.grid(row=2,column=1,padx=4,pady=4)

edit_menu.add_command(label="Find",compound=tk.LEFT,command=find_func)

font_def="Arial"
font_size_def=16

def change_font_style(main_app):
    global font_def
    font_def=font_family.get()
    text_editor.configure(font=(font_def,font_size_def))

font_box.bind("<<ComboboxSelected>>",change_font_style)

def change_font_size(main_app):
    global font_size_def
    font_size_def=size_variable.get()
    text_editor.configure(font=(font_def,font_size_def))

font_size.bind("<<ComboboxSelected>>",change_font_size)

#print(tk.font.Font(font=text_editor["font"]).actual())
def bold_func():
    text_get=tk.font.Font(font=text_editor["font"])
    if text_get.actual()["weight"]=='normal':
        text_editor.configure(font=(font_def,font_size_def,"bold"))
    if text_get.actual()["weight"]=='bold':
        text_editor.configure(font=(font_def,font_size_def,"normal"))

bold_btn.configure(command=bold_func)

def italic_func():
    text_get=tk.font.Font(font=text_editor["font"])
    if text_get.actual()["slant"]=='roman':
        text_editor.configure(font=(font_def,font_size_def,"italic"))
    if text_get.actual()["slant"]=='italic':
        text_editor.configure(font=(font_def,font_size_def,"roman"))

italic_btn.configure(command=italic_func)

def underline_func():
    text_get=tk.font.Font(font=text_editor["font"])
    if text_get.actual()["underline"]==0:
        text_editor.configure(font=(font_def,font_size_def,"underline"))
    if text_get.actual()["underline"]==1:
        text_editor.configure(font=(font_def,font_size_def,"normal"))

underline_btn.configure(command=underline_func)

def choose_color():
    color_var=tk.colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])

font_color_btn.configure(command=choose_color)

def align_left():
    text_get_all=text_editor.get(1.0,"end")
    text_editor.tag_config("left",justify=tk.LEFT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get_all,"left")

left_btn.configure(command=align_left)

def align_center():
    text_get_all=text_editor.get(1.0,"end")
    text_editor.tag_config("center",justify=tk.CENTER)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get_all,"center")

center_btn.configure(command=align_center)

def align_right():
    text_get_all=text_editor.get(1.0,"end")
    text_editor.tag_config("right",justify=tk.RIGHT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get_all,"right")

right_btn.configure(command=align_right)

status_bar=ttk.Label(main_app,text="Status Bar",anchor=tk.N)
#status_bar=ttk.Label(main_app, relief=tk.SUNKEN)
status_bar.pack(side=tk.BOTTOM,fill=tk.X)

text_change=False

def change_count(event=None):
    global text_change
    if text_editor.edit_modified():
        text_change=True
        word=len(text_editor.get(1.0,"end-1c").split())
        character=len(text_editor.get(1.0,"end-1c").replace(" ",""))
        status_bar.config(text= f"character :{character} word:{word}")
    text_editor.edit_modified(False)

text_editor.bind("<<Modified>>",change_count)
#Anina
#Creating DB for Encryption
connect = sqlite3.connect('project.db')
cur = connect.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS  EncryptionData (
   password text,
   cipher_text text,
   salt text,
   nonce text, 
   tag text
)
""")

connect.commit()
connect.close()

#Encryption
def encrypt():
    connect = sqlite3.connect('project.db')
    cur = connect.cursor()
    password = simpledialog.askstring("Create Password", "Please Enter a password for encryption")

    cur.execute("SELECT *, oid from EncryptionData")
    records = cur.fetchall()
    for r in records:
        if password==r[0]:
            password = simpledialog.askstring("Password already exists", "Please Enter a UNIQUE password for encryption")

    plain_text=text_editor.get(1.0,"end-1c")

    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))

    cipher_text_decoded = b64encode(cipher_text).decode('utf-8')
    salt_decoded = b64encode(salt).decode('utf-8')
    nonce_decoded = b64encode(cipher_config.nonce).decode('utf-8')  
    tag_decoded = b64encode(tag).decode('utf-8')
    
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,cipher_text_decoded)
    #Inserting values into db
    
    cur.execute("INSERT INTO EncryptionData VALUES(:pword, :ctext, :salt, :nonce, :tag)",
        {
            'pword': password,
            'ctext':cipher_text_decoded,
            'salt':salt_decoded,
            'nonce':nonce_decoded,
            'tag':tag_decoded
        }
    )

    connect.commit()
    connect.close()



def decrypt():
    key = simpledialog.askstring("Enter Password", "Please Enter a password for decryption")
    cipher_text=text_editor.get(1.0,"end-1c")
    #Get values from db
    connect = sqlite3.connect('project.db')
    cur = connect.cursor()
    cur.execute("SELECT *, oid from EncryptionData")
    records = cur.fetchall()
    for r in records:
        if key==r[0]:
            salt = b64decode(r[2])
            cipher_text = b64decode(r[1])
            nonce = b64decode(r[3])
            tag = b64decode(r[4])

    
    connect.commit()
    connect.close()
    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        key.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,decrypted)
    return decrypted
    

#Add Menu Item
encryption_menu = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="Encryption",menu=encryption_menu)
#Add Dropdown
encryption_menu.add_command(label="Encrypt",compound=tk.LEFT,command=encrypt)
encryption_menu.add_command(label="Decrypt",compound=tk.LEFT,command=decrypt)






main_app.mainloop()