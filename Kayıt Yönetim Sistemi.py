# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 21:29:21 2025

@author: MUSTAFA
"""
from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

#Tkinter Penceresi Ayarları
root = Tk()
root.title("Contact List")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#6666ff")

#SQL Değişkenleri
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()

#SQLite ve Veritabanı Yönetimi
def Database():
    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'member' (
            mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            firstname TEXT,
            lastname TEXT,
            gender TEXT,
            age TEXT,
            address TEXT,
            contact TEXT
            )           
                   ''') #Eğer member tablosu yoksa ekler
    cursor.execute("SELECT * FROM 'member' ORDER BY 'firstname' ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data)) #Verileri tkinter listesine ekle
    cursor.close()
    conn.close()

def SubmitData():
    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or ADDRESS.get() == "" or CONTACT.get() == "":
        tkMessageBox.showwarning('', 'Lütfen zorunlu alanları doldurun.', icon='warning')
    else:
        tree.delete(*tree.get_children()) #Ekrandaki verileri temizle
        conn = sqlite3.connect('contact.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO 'member' (firstname, lastname, gender, age, address, contact)
            VALUES(?, ?, ?, ?, ?, ?)""",
            (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), int(AGE.get()), ADDRESS.get(), CONTACT.get())
            ) #Kullanıcıdan gelen verileri kaydet
        conn.commit()
        cursor.execute("SELECT * FROM  'member' ORDER BY 'firstname' ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data)) #Ekrana yeni verileri yaz
        cursor.close()
        conn.close()
        # Formu sıfırla
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")

def UpdateData():
    if GENDER.get() == "":
        tkMessageBox.showwarning('', 'Lütfen gerekli yerleri doldurunuz', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect('contact.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE 'member' 
            SET `firstname` = ?, `lastname` = ?, `gender` = ?, `age` = ?, `address` = ?, `contact` = ?
            WHERE 'mem_id' = ?           
            """, (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get(), int(mem_id))
            )
        conn.commit()
        cursor.execute("SELECT * FROM 'member' ORDER BY 'firstname' ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        # Formu sıfırla
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")

def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus() #Seçili ögeyi al
    contents = tree.item(curItem) #Seçilen ögenin tüm elemanları dict olarak gelir
    selecteditem = contents['values'] #İçeriğin sadece değerlerini al
    mem_id = selecteditem[0] #İlk değer olan 'mem_id' değişkenine ID'yi atıyoruz
    # Formu sıfırlar
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    # Seçili veriyi forma yerleştir
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2]) 
    GENDER.set(selecteditem[3])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5]) 
    CONTACT.set(selecteditem[6])
    #Güncelleme penceresi oluştur
    UpdateWindow = TopLevel()
    UpdateWindow.title('Contact List')
    width = 400
    height = 300
    #Ekranı ortalamak için koordinatları hesapla 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width / 2) + 450) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    # Güncelleme penceresinin boyutunu ve konumunu ayarla
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()
    #===================FRAMES==============================
    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)   
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text='Male', variable=GENDER, value='Male', font=('arial', 14))
    Male.pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text='Female', variable=GENDER, value='Female', font=('arial', 14))
    Female.pack(side=LEFT)
    #===================LABELS==============================
    lbl_firstname = Label(ContactForm, text="Ad", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="Soyad", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(ContactForm, text="Cinsiyet", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_age = Label(ContactForm, text="Yas", font=('arial', 14), bd=5)
    lbl_age.grid(row=3, sticky=W)
    lbl_address = Label(ContactForm, text="Adres", font=('arial', 14), bd=5)
    lbl_address.grid(row=4, sticky=W)
    lbl_contact = Label(ContactForm, text="Tel No", font=('arial', 14), bd=5)
    lbl_contact.grid(row=5, sticky=W)
    #===================GRİDS==============================
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)  # Cinsiyet butonlarını yerleştir
    age = Entry(ContactForm, textvariable=AGE, font=('arial', 14))
    age.grid(row=3, column=1)
    address = Entry(ContactForm, textvariable=ADDRESS, font=('arial', 14))
    address.grid(row=4, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT, font=('arial', 14))
    contact.grid(row=5, column=1)
    # Güncelleme butonu
    btn_updatecon = Button(ContactForm, text="Guncelle", width=50, command=UpdateData)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)
    
def DeleteData():
    if not tree.selection():
        tkMessageBox.showwarning('', 'Seçim yapmanız gerekiyor!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Bu kaydı gerçekten silmek istiyor musunuz?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = tree.item(curItem)
            selectedItem = contents['values']
            tree.delete(curItem)
            
            conn = sqlite3.connect('contact.db')
            cursor = conn.cursor()
            #Seçili kaydı db'den sil
            cursor.execute("DELETE FROM 'member' WHERE 'mem_id' = %d" % selectedItem[0])
            conn.commit()
            cursor.close()
            conn.close()
def AddNewWindow():
    global NewWindow
    # Form alanlarını sıfırla
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")

    NewWindow = Toplevel()
    NewWindow.title("Contact List")
    width = 400
    height = 300

    # Ekranı ortalamak için koordinatları hesapla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width / 2) - 455) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)

    # Pencereyi ayarla
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))

    # Eğer güncelleme penceresi açıksa, kapat
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()    
    #===================FRAMES==============================
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="Erkek", variable=GENDER, value="Male",  font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Kadın", variable=GENDER, value="Female",  font=('arial', 14)).pack(side=LEFT)
    
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="Yeni Kayıt Ekleme", font=('arial', 16), bg="#66ff66",  width = 300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="Ad", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="Soyad", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(ContactForm, text="Cinsiyet", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_age = Label(ContactForm, text="Yas", font=('arial', 14), bd=5)
    lbl_age.grid(row=3, sticky=W)
    lbl_address = Label(ContactForm, text="Adres", font=('arial', 14), bd=5)
    lbl_address.grid(row=4, sticky=W)
    lbl_contact = Label(ContactForm, text="Tel No", font=('arial', 14), bd=5)
    lbl_contact.grid(row=5, sticky=W)

    #===================ENTRY===============================
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    age = Entry(ContactForm, textvariable=AGE,  font=('arial', 14))
    age.grid(row=3, column=1)
    address = Entry(ContactForm, textvariable=ADDRESS,  font=('arial', 14))
    address.grid(row=4, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT,  font=('arial', 14))
    contact.grid(row=5, column=1)
    

    #==================BUTTONS==============================
    btn_addcon = Button(ContactForm, text="Kaydet", width=50, command=SubmitData)
    btn_addcon.grid(row=6, columnspan=2, pady=10)

    
#Ana arayüz
#============================FRAMES======================================
Top = Frame(root, width=500, bd=1, relief=SOLID)  
Top.pack(side=TOP)
Mid = Frame(root, width=500, bg='#6666ff')
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="#6666ff")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)   
#============================LABELS======================================
lbl_title = Label(Top, text="Kayıt Yönetim Sistemi", font=('arial', 16), width=500)
lbl_title.pack(fill=X)
#============================BUTTONS=====================================
btn_add = Button(MidLeft, text="+ YENİ KAYIT EKLE", bg="#66ff66", command=AddNewWindow)
btn_add.pack()
btn_delete = Button(MidRight, text="KAYIT SİL", bg="red", command=DeleteData)
btn_delete.pack(side=RIGHT)

#============================TABLES======================================
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Firstname', text="Ad", anchor=W)
tree.heading('Lastname', text="Soyad", anchor=W)
tree.heading('Gender', text="Cinsiyet", anchor=W)
tree.heading('Age', text="Yas", anchor=W)
tree.heading('Address', text="Adres", anchor=W)
tree.heading('Contact', text="Tel No", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.column('#6', stretch=NO, minwidth=0, width=120)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)
   
if __name__ == '__main__':
    Database()
    root.mainloop()

