import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import csv
from datetime import datetime
import os

class Noted():

	def __init__(self):
		self.AppNoted = tk.Tk()
		self.AppNoted.title('')
		self.AppNoted.resizable(0,0)
		self.AppNoted.config(bg='gray80')
		self.Header = Label(self.AppNoted, text='Noted', font=("Arial",20,"bold"),bg='gray80', fg='RoyalBlue4', pady=10).pack()
		self.ViewDb()
		self.dbFile()

		self.AppNoted.mainloop()



	def ViewDb(self):

		def Tambah():
			Date = datetime.today().strftime('%d-%m-%Y')
			Noted = inputCatatan.get()
			Pandas().Tambah(date=Date, noted=Noted)

			# delete previos list
			for i in self.listBox.get_children():
				self.listBox.delete(i)
			
			# ambil no dan placeholder
			self.pilihanHapus = ttk.Combobox(self.frameboth, width=12, value= tuple(self.getindex()))
			self.pilihanHapus.grid(column=5, row=1)

			self.dbFile()


		def Hapus():
			numb = int(self.pilihanHapus.get()) - 1
			Pandas().Hapus(numb=numb)

			# delete previos list
			for i in self.listBox.get_children():
				self.listBox.delete(i)

			# update list
			self.pilihanHapus = ttk.Combobox(self.frameboth, width=12, value= tuple(self.getindex()))
			self.pilihanHapus.grid(column=5, row=1)

			self.dbFile()

		def headerView():
			self.frame = Canvas(self.AppNoted, width=self.AppNoted.winfo_reqwidth(), height=self.AppNoted.winfo_reqheight())
			self.frame.pack()
			# listview
			self.listBox = ttk.Treeview(self.frame, selectmode="extended", columns=('No','Date','Noted'),show='headings',height=10)

			# scrool
			self.Scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.listBox.yview)
			self.Scroll.pack(side='right', fill='y')
			self.listBox.configure(yscrollcommand=self.Scroll.set)

			self.style = ttk.Style(self.AppNoted)
			self.style.configure(".", font=('Helvetica', 8), foreground="black")
			self.style.configure("Treeview.Heading", foreground='white',background='RoyalBlue1',font=("Arial",10))  # <----
	        # insert heading
			self.listBox.heading('No', text='No')
			self.listBox.column('No', minwidth=50, width=50, stretch=YES)
			self.listBox.heading('Date', text='Date')
			self.listBox.column('Date', minwidth=130, width=130, stretch=YES)
			self.listBox.heading('Noted', text='Noted')
			self.listBox.column('Noted', minwidth=600, width=600, stretch=YES)
			self.listBox.pack()

		headerView()

		self.frameboth = Canvas(self.AppNoted, width=self.AppNoted.winfo_reqwidth(), height=50, bg='gray80',highlightthickness=0,borderwidth=2 )
		self.frameboth.pack()

		labelHeaderAksi = Label(self.frameboth, text='Aksi', font=("Arial",15,"bold"), bg='gray80').grid(column=0, row=0, columnspan=7)
		labelTambah = Label(self.frameboth, text='Tambah catatan', bg='gray80').grid(column=0, row=1,padx=5)
		inputCatatan = Entry(self.frameboth,)
		inputCatatan.grid(column=1, row=1,padx=5)
		btnTambah = Button(self.frameboth, text='Tambah',bg='RoyalBlue1', fg='white', command=Tambah).grid(column=2, row=1, pady=10,padx=5)

		labelPemisah = Label(self.frameboth, text='||', bg='gray80').grid(column=3,row=1,padx=5)

		labelHapus = Label(self.frameboth, text='Hapus catatan', bg='gray80').grid(column=4,row=1,padx=5)
		
		# ambil no dan placeholder
		self.pilihanHapus = ttk.Combobox(self.frameboth, width=12, value= tuple(self.getindex()))
		self.pilihanHapus.grid(column=5, row=1)

		btnHapus = Button(self.frameboth, text='Hapus',bg='RoyalBlue1', fg='white', command=Hapus).grid(column=6, row=1,padx=5)
		btnExit = Button(self.frameboth, text='Exit',bg='red', fg='white', padx=25, pady=5,command=lambda:self.AppNoted.destroy()).grid(column=6, row=2, pady=10)


	def dbFile(self):
		try :

			# sorted
			Pandas().Sort()
			file = 'file/Noted.csv'
			with open(file) as f:

				reader = csv.DictReader(f, delimiter=',')
				no = 1

				for row in reader:
					
					DB = []
					DB.append(no)
					DB.append(row['Date'])
					DB.append(row['Noted'])

					no += 1
					self.listBox.insert("", "end", values=tuple(DB))
		
		except:
			df = pd.DataFrame(
	    		data={
	    			"Date": [], 
	    			"Noted": []
	    		}
	    	)
			df.to_csv("file/Noted.csv",index=False)

	def getindex(self):

		file = 'file/Noted.csv'
		with open(file) as f:

			reader = csv.DictReader(f, delimiter=',')
			no = []
			index = 1
			for row in reader:
				
				no.append(index)
				index += 1

		return no		

		

class Pandas():

	def __init__(self):
		self.path = 'file/Noted.csv'
		self.mydatafile = pd.read_csv(self.path)

	def Sort(self):
		data = self.mydatafile.sort_values(str('Date'))
		data.to_csv(str(self.path), index=False)

	def Tambah(self, date, noted):
		tambahNoted = {'Date': date,'Noted': noted}
		tambahNoted = self.mydatafile.append(tambahNoted, ignore_index=True)
		tambahNoted.to_csv(str(self.path), index=False)

	def Hapus(self, numb):
		delete = self.mydatafile.drop(self.mydatafile.index[[numb]])
		delete.to_csv(str(self.path), index=False)
		