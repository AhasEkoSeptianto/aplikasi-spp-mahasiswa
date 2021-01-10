from tkinter import *
from tkinter import ttk ,messagebox
import tkinter as tk
from PIL import Image,ImageTk
import webbrowser
import csv
import time
from datetime import datetime,time
from .myCsv import myCsv,pandas
from .Noted import Noted
import os

class Spp():

    def __init__(self):
        # require tkinter algoritm
        self.root = Tk()
        self.root.title('Spp Mahasiswa')
        try :
            # auto maximaze windows
            self.root.attributes('-zoomed', True)
        except :
            # auto maximisze linux because iam use linux 
            self.root.attributes('-fullscreen', True)
            
        self.root.configure(bg='snow')
        self.root.minsize(1100,600)

        # Set cureent screen height and width
        self.winwidth = self.root.winfo_screenwidth()
        self.winheight = self.root.winfo_screenheight()

        # pandas
        self.myFilesCsv = myCsv()
        self.pandas = pandas()
        self.getAllName()

        self.utility()
        self.viewDBHeader()
        self.position()

        # bind
        # left label
        self.logo.bind("<Enter>", self.on_enter)
        self.logo.bind("<Leave>", self.on_leave)

        # right label
        self.ChooseSemester.bind('<<ComboboxSelected>>', self.viewDBHeader)
        self.SortingBy.bind('<<ComboboxSelected>>', self.UpdateTable)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update_clock()
        self.root.mainloop()

    def utility(self):
    # left mode
        self.leftMode = Canvas(self.root, width=self.winwidth/4,height=self.winheight*2, bg='gray80' )

        #image
        logo = Image.open('img/logo.png')
        logo = logo.resize((110,110), Image.ANTIALIAS)
        logo_pil = ImageTk.PhotoImage(logo)
        self.logo = Button(self.leftMode, image=logo_pil, bg='gray80',height=300, width=self.winwidth, command=lambda : webbrowser.open('https://web.stikomcki.ac.id/'))
        self.logo.image = logo_pil

        #label logo
        self.labelLogo = Label(self.leftMode, text='Sekolah Tinggi Ilmu Komputer\nCipta Karya Informatika', bg='gray80')
        self.Timer = Label(self.leftMode, text='', font=("Arial",15), bg='gray80', fg='RoyalBlue4')

        # button left mode
        self.buttonPembayaran = Button(self.leftMode, text='Pembayaran', height=3, width=20, font=("System", 10),bg='RoyalBlue1', fg='white', padx=110, command=self.Pembayaran)
        self.buttonTambah = Button(self.leftMode, text='Tambah Mahasiswa', height=3,width=20,font=("System", 10), bg='RoyalBlue1',fg='white', padx=110, command=self.TambahBtn)
        self.buttonUbah = Button(self.leftMode, text='Ubah Mahasiswa',height=3, width=20, font=("System", 10),  bg='RoyalBlue1',fg='white', padx=110, command=self.UbahBtn)
        self.buttonHapus = Button(self.leftMode, text='Hapus Mahasiswa',height=3, width=20, font=("System", 10),  bg='RoyalBlue1',fg='white', padx=110, command=self.HapusBtn)
        self.buttonNoted = Button(self.leftMode, text='Catatan', height=3, width=20, font=("System", 10),bg='RoyalBlue1', fg='white', padx=110, command=lambda:Noted())
        self.clearForm = Button(self.leftMode, text='Clear Form', height=3, width=20, font=("System", 10),  bg='RoyalBlue1',fg='white', padx=110, command=self.clearAllForm)
        self.exit = Button(self.leftMode, text='Exit', height=3, width=20, font=("System", 10), bg='RoyalBlue1',fg='white', padx=110, command=self.on_closing)

    # RRight mode
        self.rightMode = Canvas(self.root, width=1042, height=self.winheight*2)

        # view db
        self.listBox = ttk.Treeview(self.rightMode, selectmode="extended", columns=(),
                                    show='headings',
                                    height=10)
        # Combobox Semester
        self.posSemester = tk.StringVar()
        self.ChooseSemester = ttk.Combobox(self.rightMode, width=10, textvariable=self.posSemester)
        self.ChooseSemester['values'] = ('Semester 1','Semester 2','Semester 3','Semester 4','Semester 5','Semester 6','Semester 7','Semester 8')
        self.ChooseSemester.current(0)

        # Sort
        self.filtering = tk.StringVar()
        self.SortingBy = ttk.Combobox(self.rightMode, width=10, textvariable=self.filtering)
        self.SortingBy['values'] = ('Nim','Nama','Jurusan')
        self.SortingBy.current(0)


        # label
        self.labelSpp = Label(self.rightMode, text='SPP Mahasiswa', font=("Arial",15))
        self.labelSemester = Label(self.rightMode, text='Semester', font=("Arial",10))
        self.labelSorting = Label(self.rightMode, text='Urut', font=("Arial",10))
    # Both Mode
        self.bothMode = Canvas(self.rightMode, width=980, height=180)

    def viewDBHeader(self,event='None'):
        def changeValueDB(Header):
            # disini definisi jika list sudah ada sebelumnya , jika ada maka akan dihapus dan dibuat baru
            try :
                self.listBox.destroy()
            except:
                pass

            # definisi treeview untuk lembar kerja
            self.listBox = ttk.Treeview(self.rightMode, selectmode="extended", columns=Header,
                                        show='headings',
                                        height=20)
            # scrool bar
            self.Scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.listBox.yview)
            self.Scroll.place(x=1335, y=90, height=420)
            self.listBox.configure(yscrollcommand=self.Scroll.set)

            self.style = ttk.Style()
            self.style.configure(".", font=('Helvetica', 8), foreground="black")
            # self.style.configure("Treeview", foreground='red')
            self.style.configure("Treeview.Heading", foreground='white',background='RoyalBlue1',font=("Arial",10))  # <----

            # insert value ke lembar kerja
            for i in Header:
                if i == 'Nim'  :
                    self.listBox.heading(i, text=i)
                    self.listBox.column(i.title(), minwidth=110, width=110, stretch=YES)
                    continue

                if i == 'Nama' :
                    self.listBox.heading(i, text=i)
                    self.listBox.column(i.title(), minwidth=230, width=230, stretch=YES)
                    continue

                self.listBox.heading(i, text=i)
                self.listBox.column(i.title(), minwidth=80, width=80, stretch=YES)

            # give bigger row name


            self.listBox.place(relx=0.5, y=1040, anchor=CENTER)

        listHeaderTable = ()

        # filtering user input
        if self.ChooseSemester.get() == 'Semester 1' :listHeaderTable = ('No', 'Nim', 'Nama', 'Jurusan', 'Spp 1', 'Spp 2', 'Spp 3', 'Spp 4', 'Spp 5', 'Spp 6')
        if self.ChooseSemester.get() == 'Semester 2' :listHeaderTable = ('No', 'Nim', 'Nama', 'Jurusan', 'Spp 7', 'Spp 8', 'Spp 9', 'Spp 10', 'Spp 11', 'Spp 12')
        if self.ChooseSemester.get() == 'Semester 3' :listHeaderTable = ('No', 'Nim', 'Nama', 'Jurusan', 'Spp 13', 'Spp 14', 'Spp 15', 'Spp 16', 'Spp 17', 'Spp 18')
        if self.ChooseSemester.get() == 'Semester 4':listHeaderTable = ('No', 'Nim', 'Nama', 'Jurusan', 'Spp 19', 'Spp 20', 'Spp 21', 'Spp 22', 'Spp 23', 'Spp 24')
        if self.ChooseSemester.get() == 'Semester 5':listHeaderTable = ('No', 'Nim', 'Nama', 'Jurusan', 'Spp 25', 'Spp 26', 'Spp 27', 'Spp 28', 'Spp 29', 'Spp 30')
        if self.ChooseSemester.get() == 'Semester 6' :listHeaderTable = ('No', 'Nim', 'Nama', 'Jurusan', 'Spp 31', 'Spp 32', 'Spp 33', 'Spp 34', 'Spp 35', 'Spp 36')
        if self.ChooseSemester.get() == 'Semester 7' :listHeaderTable = ('No', 'Nim', 'Nama', 'Jurusan', 'Spp 37', 'Spp 38', 'Spp 39', 'Spp 40', 'Spp 41', 'Spp 42')
        if self.ChooseSemester.get() == 'Semester 8' :listHeaderTable = ('No', 'Nim', 'Nama', 'Jurusan', 'Spp 43', 'Spp 44', 'Spp 45', 'Spp 46', 'Spp 47', 'Spp 48')

        changeValueDB(listHeaderTable)
        self.UpdateTable()

    def position(self):
    # left
        self.leftMode.place(x=150,y=30, anchor=CENTER)
        self.logo.place(relx=0.5, y=self.winheight+30, anchor=CENTER)
        #image

        # Label logo
        self.labelLogo.place(relx=0.5,y=self.winheight+120, anchor=CENTER)
        self.Timer.place(relx=0.5, y=self.winheight + 585, anchor=CENTER)

        # button place
        self.buttonPembayaran.place(relx=0.5,y=self.winheight + 205, anchor=CENTER)
        self.buttonTambah.place(relx=0.5, y=self.winheight + 265, anchor=CENTER)
        self.buttonUbah.place(relx=0.5, y=self.winheight + 325, anchor=CENTER)
        self.buttonHapus.place(relx=0.5, y=self.winheight + 385, anchor=CENTER)
        self.buttonNoted.place(relx=0.5, y=self.winheight + 445, anchor=CENTER)
        self.clearForm.place(relx=0.5, y=self.winheight + 505, anchor=CENTER)
        self.exit.place(relx=0.5, y=self.winheight + 665, anchor=CENTER)

    # right
        self.rightMode.place(x=844,y=30, anchor=CENTER)

        # label
        self.labelSpp.place(relx=0.5, y=800, anchor=CENTER)
        self.labelSemester.place(relx=0.8, y=780, anchor="s")
        self.labelSorting.place(relx=0.8, y=810, anchor="s")

        # Combobox Semester
        self.ChooseSemester.place(relx=0.9, y=780, anchor="s")
        self.SortingBy.place(relx=0.9, y=810, anchor="s")



    def UpdateTable(self, path=None, filter=None):
        global DB
        def insertSpp(index):
            for i in range(6):
                postRow = 'Spp' + str(index)
                DB.append(row[postRow])
                index += 1

        path = str(self.ChooseSemester.get()) + '.csv'
        Sort = self.SortingBy.get()

        # Sorting Csv
        try:
            self.pandas.Sorting(sortby=Sort)
        except :
            pass

        # delete previos list
        for i in self.listBox.get_children():
            self.listBox.delete(i)

        # define is filter

        if filter :
            self.pandas.Filter(listName=filter)
            file = 'file/filter.csv'

        else:
            file = 'file/Spp Mahasiswa.csv'

        # read files
        with open(file) as f:
                reader = csv.DictReader(f, delimiter=',')
                no = 1

                for row in reader:

                    # loop for effesiency
                    DB = []
                    DB.append(no)
                    DB.append(row['Nim'])
                    DB.append(row['Nama'])
                    DB.append(row['Jurusan'])

                    # 1 is index from 1 to 6 for semester 1 and 7 to 12 for semester 2 and etc
                    if path == 'Semester 1.csv': insertSpp(1)
                    if path == 'Semester 2.csv': insertSpp(7)
                    if path == 'Semester 3.csv': insertSpp(13)
                    if path == 'Semester 4.csv': insertSpp(19)
                    if path == 'Semester 5.csv': insertSpp(25)
                    if path == 'Semester 6.csv': insertSpp(31)
                    if path == 'Semester 7.csv': insertSpp(37)
                    if path == 'Semester 8.csv': insertSpp(43)

                    self.listBox.insert("", "end", values=tuple(DB))

                    no += 1

    def Pembayaran(self):

        self.clearAllForm()

        def filtering():
            # get user input
            key = self.InputFiltering.get().rstrip()
            keylen = len(key)

            namaAlter = self.AlterName(key)

            # variable
            semuanama = self.getAllName()
            namaFilter = []
            index = 0

            # filtering jika form telah diisi
            if namaAlter:
                # run ketika form lebih dari 0
                if len(namaAlter) > 0:

                    if namaAlter != 'Nama' :
                        for i in range(len(semuanama)-1) :

                            if namaAlter == semuanama[i][:keylen] :
                  
                                namaFilter.append(semuanama[i])
                    else:
                        for i in range(len(semuanama)-1) :
                          namaFilter.append(semuanama[i])
                                   
            else :
                for i in range(len(semuanama)-1) :
                    namaFilter.append(semuanama[i])
                       

            # delete previos filtering and create agains
            self.canvasPilihMhs.destroy()
            
            # canvas untuk filtering
            self.canvasPilihMhs = Canvas(self.bothModeLeft, height=130, highlightthickness=1,borderwidth=5, relief="ridge", bg='gray80')
            self.canvasPilihMhs.place(relx=0.5, rely=0.6, anchor=CENTER)
        
            self.labelFilter = Label(self.canvasPilihMhs, text='Pilih Mahasiswa').place(relx=0.2, rely=0.5, anchor='s')
        
            # pilih mahasiswa
            pilihMhs = tk.StringVar()
            self.pilihanMhs = ttk.Combobox(self.canvasPilihMhs, width=20, textvariable=pilihMhs)
            self.pilihanMhs['value'] = tuple(namaFilter)
            self.pilihanMhs.place(relx=0.7, rely=0.5, anchor="s")
            
            self.UpdateTable(filter=namaFilter)
            self.pilihanMhs.bind('<<ComboboxSelected>>', sppAnswert)

            return True

        def sppAnswert(event):
            nama = self.pilihanMhs.get()
            spp = pilihanSpp.get()

            # get int spp
            spp = spp.replace("Spp ","")
            
            if nama != "" and spp != "" :
                SppMasiswa = self.pandas.getSpp(nama,int(spp))
                if SppMasiswa == "~" : 
                    hasilJawabSpp.set("")
                else :
                    hasilJawabSpp.set( "Notice !!\n" + nama + " : " + SppMasiswa)


        def bayar():
            nama = self.pilihanMhs.get()
            sppPos = pilihanSpp.get()
            # hilangkan space
            sppPos = sppPos.replace(" ","")
            bayar = inputPembayaran.get()
        
            if nama != '' and sppPos != '' and bayar != '' :
                self.pandas.Pembayaran(name=nama, sppPos=sppPos, spp=bayar)
                tk.messagebox.showinfo('info', 'berhasil')
        
            self.UpdateTable()

        def on_click(event):
            self.InputFiltering.configure(state=NORMAL)
            self.InputFiltering.delete(0, END)
            # make the callback only work once
            self.InputFiltering.unbind('<Button-1>', on_click_filter)


        # filtering data

        # place x == seperempat
        setengah = self.rightMode.winfo_reqwidth()/2
        seperempat = self.rightMode.winfo_reqwidth()/2/2

        # canvas untuk pembayaran Kiri
        self.bothModeLeft = Canvas(self.rightMode, width=(self.rightMode.winfo_reqwidth()/2), height=180, highlightthickness=0)
        self.bothModeLeft.place(x=seperempat,y=1350, anchor=CENTER)

    # filter

        self.labelFiltering = Label(self.bothModeLeft, text='Filter ').place(relx=0.3, y=10, anchor=CENTER)
        
            # get value from StringVar()
        self.InputFiltering = Entry(self.bothModeLeft,)
        self.InputFiltering.place(relx=0.5, y=10, anchor=CENTER)
            # placeholder
        self.InputFiltering.insert(0, "Nama")
        self.InputFiltering.configure(state=DISABLED)

        # btn for filtering
        self.buttonFilter = Button(self.bothModeLeft, text='Submit', command=filtering,bg='RoyalBlue1', fg='white').place(relx=0.8, y=10, anchor=CENTER)
        
    # leftboth form
        # canvas didalam canvas
        self.canvasPilihMhs = Canvas(self.bothModeLeft, height=130, highlightthickness=0,borderwidth=5, relief="ridge", bg='gray80')
        self.canvasPilihMhs.place(relx=0.5, rely=0.6, anchor=CENTER)

        # pilih mahasiswa
        self.labelFilter = Label(self.canvasPilihMhs, text='Pilih Mahasiswa').place(relx=0.2, rely=0.5, anchor='s')
        
        pilihMhs = tk.StringVar()
        self.pilihanMhs = ttk.Combobox(self.canvasPilihMhs, width=20, textvariable=pilihMhs, value=self.getAllName())
        self.pilihanMhs.place(relx=0.7, rely=0.5, anchor="s")


    # rightboth form
        
        # canvas untuk pembayaran Kanan
        self.bothModeRight = Canvas(self.rightMode, width=(self.rightMode.winfo_reqwidth()/2), height=180, highlightthickness=0,borderwidth=5, relief="ridge")
        self.bothModeRight.place(x=setengah+seperempat - 20,y=1350, anchor=CENTER)

        self.labelHeaderAksi = Label(self.bothModeRight, text='Aksi', font=("Arial",15)).place(relx=0.5, rely=0.2, anchor='s')
        
        labelPilihSpp = Label(self.bothModeRight, text='Pilih Spp').place(relx=0.1, rely=0.5, anchor="s")
        
        # ambil spp
        pilihSpp = tk.StringVar()
        pilihanSpp = ttk.Combobox(self.bothModeRight, width=12, textvariable=pilihSpp)
        
        sppRange = []
        for i in  range(1,49):
            spp = 'Spp ' + str(i)
            sppRange.append(spp)

        pilihanSpp['value'] = tuple(sppRange) 
        pilihanSpp.place(relx=0.3, rely=0.5, anchor="s")

        # label notice spp
        hasilJawabSpp = StringVar()
        labelJawabanSpp = Label(self.bothModeRight, textvariable=(hasilJawabSpp), fg='RoyalBlue4').place(relx=0.7, rely=0.5, anchor="s")

        labelPembayaran = Label(self.bothModeRight, text='Pilih Aksi').place(relx=0.1, rely=0.8, anchor="s")


        inputPembayaran = ttk.Combobox(self.bothModeRight, width=12, value=('Lunas','Belum Lunas', '~'))
        inputPembayaran.place(relx=0.3, rely=0.8, anchor="s")

        buttonPembayaran = Button(self.bothModeRight, text='Sumbit', bg='RoyalBlue1', fg='white', command=bayar).place(relx=0.7, rely=0.8, anchor="s")

    # bind 
        on_click_filter = self.InputFiltering.bind('<Button-1>', on_click)
        pilihanSpp.bind('<<ComboboxSelected>>', sppAnswert)
        self.pilihanMhs.bind('<<ComboboxSelected>>', sppAnswert)


    def TambahBtn(self):
        self.clearAllForm()
        # func for add mahasiswa
        def tambahsiswa():
            #  get nama
            nama = self.InputNama.get().rstrip()
            
            # change name form
            nama = self.AlterName(name=nama)

            jurusan = self.InputJurusan.get()

            # check jika nim integer
            try:
                nim = int(self.InputNim.get())
                if nama != "" and nim != "" and jurusan != "":
                    # save form
                    self.pandas.Create(nama=nama, nim=nim, jurusan=jurusan)

                    # label pesan
                    messagebox.showinfo('info', 'Berhasil menambahkan 1 Mahasiswa')
                    # update for all name
                    self.getAllName()

            except:
                nim = self.InputNim.get()
                if nim != "":messagebox.showerror('error', 'Nim harus berupa angka')


            self.UpdateTable()

        # canvas form adding siswa
        self.bothMode = Canvas(self.rightMode, width=980, height=180, highlightthickness=0)
        self.bothMode.place(relx=0.5,y=1350, anchor=CENTER)

        self.labelHeader = Label(self.bothMode, text='Tambah Mahasiswa',font=("Arial",15)).grid(column=0, row=0, columnspan=3, pady=20)

        self.LabelNama = Label(self.bothMode, text='Nama Mahasiswa  ').grid(row=1, column=0, sticky='W', pady=1, padx=40)
        self.InputNama = Entry(self.bothMode, )
        self.InputNama.grid(row=1, column=1, sticky='W', pady=1, padx=40)

        self.LabelNim = Label(self.bothMode, text='Nim Mahasiswa ').grid(row=2, column=0, sticky='W', pady=1, padx=40)
        self.InputNim = Entry(self.bothMode, )
        self.InputNim.grid(row=2, column=1, sticky='W', pady=1, padx=40)

        self.labelJurusan = Label(self.bothMode, text='Jurusan Mahasiswa').grid(row=3,column=0)
        self.getJurusan = tk.StringVar()
        self.InputJurusan = ttk.Combobox(self.bothMode, width=20, textvariable=self.getJurusan)
        self.InputJurusan['values'] = ('TI','SI')
        self.InputJurusan.current(0)
        self.InputJurusan.grid(row=3, column=1, sticky='W', pady=1, padx=40)

        # save button
        self.SubmitTambahMahasiswa = Button(self.bothMode, text='Submit', command=tambahsiswa, padx=10, pady=1,bg='RoyalBlue1', fg='white').grid(row=2, column=2, sticky='W', pady=10, padx=40)

    def UbahBtn(self):
        self.clearAllForm()

        # func for button
        def UbahMhs():
            namaMahasiswa = self.NamaMhs.get()
            ubahMhsNama = self.InputMhsNama.get()
            
            # change form input
            ubahMhsNama = self.AlterName(name=ubahMhsNama)
            ubahMhsNim = self.InputMhsNim.get()
            ubahMhsJurusan = self.InputMhsJurusan.get()

            MsgBox = tk.messagebox.askquestion('hapus mahasiswa', 'apa anda yakin ?', icon='warning')
            if MsgBox == 'yes' :
                # goto class
                self.pandas.UbahMhs(nama=namaMahasiswa, nimUbah=ubahMhsNim, namaUbah=ubahMhsNama, jurusanUbah=ubahMhsJurusan)
                messagebox.showinfo('info', 'Berhasil dirubah')

            self.UpdateTable()

        semuanama = []
        path = 'file/Spp Mahasiswa.csv'

        # get all name exist
        with open(path) as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                semuanama.append(row['Nama'])

        # canvas form change Mhs
        self.bothMode = Canvas(self.rightMode, width=980, height=180, highlightthickness=0)
        self.bothMode.place(relx=0.5,y=1350, anchor=CENTER)

        self.labelHeader = Label(self.bothMode, text='Ubah Mahasiswa',font=("Arial",15)).grid(column=0, row=0, columnspan=7, pady=10)

        self.labelNamaMhs = Label(self.bothMode, text='Pilih Mahasiswa ').grid(row=1, column=1)

        self.StringNama = tk.StringVar()
        self.NamaMhs = ttk.Combobox(self.bothMode, width=25,
                                                            textvariable=self.StringNama)
        self.NamaMhs['value'] = tuple(semuanama)
        self.NamaMhs.grid(row=1, column=2, pady=15)

        self.LabelInputNama = Label(self.bothMode, text='Nama Mahasiswa {Baru}', width=25).grid(row=2, column=0)
        self.InputMhsNama = Entry(self.bothMode,)
        self.InputMhsNama.grid(row=2, column=1, pady=2)

        self.LabelInputNim = Label(self.bothMode, text='Nim Mahasiswa {Baru}', width=25).grid(row=3, column=0)
        self.InputMhsNim = Entry(self.bothMode,)
        self.InputMhsNim.grid(row=3, column=1, pady=2)

        self.LabelInputJurusan = Label(self.bothMode, text='Jurusan Mahasiswa', width=15).grid(row=2, column=3)

        self.getJurusan = tk.StringVar()
        self.InputMhsJurusan = ttk.Combobox(self.bothMode, width=10, textvariable=self.getJurusan)
        self.InputMhsJurusan['values'] = ('TI','SI')
        self.InputMhsJurusan.current(0)
        self.InputMhsJurusan.grid(row=2, column=4, pady=2)



        self.ubahMhs = Button(self.bothMode, text='Submit form', command=UbahMhs, padx=30,bg='RoyalBlue1', fg='white').grid(row=3, column=3)


    def HapusBtn(self):
        self.clearAllForm()

        # func for get all name
        def semuaNama():
            semuanama = []
            path = 'file/Spp Mahasiswa.csv'
            with open(path) as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    nama = row['Nama']
                    semuanama.append(nama)

            return semuanama

        def hapusSiswa():
            nama = hapusMahasiswaEntry.get()
            MsgBox = tk.messagebox.askquestion('hapus mahasiswa', 'hapus {} ?'.format(nama), icon='warning')

            if MsgBox == 'yes':
                self.pandas.Delete(nama=nama)
                semuanama = semuaNama()
                hapusMahasiswaEntry['value'] = tuple(semuanama)
                text = 'Mahasiswa ' + nama + ' berhasil dihapus'
                tk.messagebox.showinfo('info', text)

            else:
                tk.messagebox.showinfo('info', 'mahasiswa tidak dihapus')

            self.UpdateTable()

        # getting all name
        semuanama = semuaNama()

        # canvas form delete siswa
        self.bothMode = Canvas(self.rightMode, width=980, height=180, highlightthickness=0)
        self.bothMode.place(relx=0.5, y=1350, anchor=CENTER)

        labelHeader = Label(self.bothMode, text='Hapus Mahasiswa',font=("Arial",15)).grid(column=0, row=0, columnspan=3, pady=30)

        LabelHapusSiswa = Label(self.bothMode, text='Pilih Mahasiswa : ')
        LabelHapusSiswa.grid(column=0, row=1,sticky='W', padx=20)

        pilihMhs = tk.StringVar()
        hapusMahasiswaEntry = ttk.Combobox(self.bothMode, width=30, textvariable=pilihMhs)
        hapusMahasiswaEntry['value'] = tuple(semuanama)
        hapusMahasiswaEntry.grid(column=1, row=1, sticky='W')

        hapusMahasiswaBtn = Button(self.bothMode, text='Submit', command=hapusSiswa,bg='RoyalBlue1', fg='white')
        hapusMahasiswaBtn.grid(column=2, row=1, pady=10, padx=20)


    def AlterName(self,name):
        # here is change upper and letter key
        namaAlter = ''
        # change Name String
        index = 0
        for char in name :

            # index [0] == upper
            if index == 0:
                namaAlter += char.upper()
                index += 1
                continue

            # jika ketemu spasi maka diubah menjadi upper
            if name[index -1] == " ":
                namaAlter += char.upper()
                index += 1
                continue

            namaAlter += char.lower()
            index += 1

        return namaAlter

    def clearAllForm(self):
        try :
            self.bothMode.destroy()
            self.bothModeLeft.destroy()
            self.bothModeRight.destroy()
        except:
            pass

    def on_enter(self,e):
        self.labelLogo.config(bg='snow2')
        # header BD

    def on_leave(self,e):
        self.labelLogo.config(bg='gray80')

    # if wont to closing
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            try:
                os.remove('file/filter.csv')
            except :
                pass

    def getAllName(self):

        #  get all name
        self.semuaMhs = []
        path = 'file/Spp Mahasiswa.csv'

        # get all name exist
        with open(path) as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                self.semuaMhs.append(row['Nama'])

        return self.semuaMhs

    def update_clock(self):
        day = datetime.today().strftime("%A")
        time = datetime.today().strftime('%d-%m-%Y')
        now_clock = datetime.now().strftime('%H:%M:%S')
        show = day + ' : ' + time + '\n' + now_clock
        self.Timer.configure(text=show)
        self.root.after(1000, self.update_clock)

