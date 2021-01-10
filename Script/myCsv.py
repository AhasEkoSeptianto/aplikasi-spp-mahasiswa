import pandas as pd
from tkinter import messagebox
import os

class myCsv():

    def __init__(self):

        try:
            os.chdir('file/')
            # try to open file if exist
            with open('Spp Mahasiswa.csv') as f:
                pass

            os.chdir('../')

        except:
            self.CreateFiles()
            os.chdir('../')

    def CreateFiles(self, path=None):

        mydataCsv = {
            'Nama': [],
            'Nim': [],
            'Jurusan': [],
            'Spp 1': [], 'Spp 2': [], 'Spp 3': [], 'Spp 4': [], 'Spp 5': [], 'Spp 6': [], 'Spp 7': [], 'Spp 8': [], 'Spp 9': [], 'Spp 10': [], 'Spp 11': [],
            'Spp 12': [], 'Spp 13': [], 'Spp 14': [], 'Spp 15': [], 'Spp 16': [],'Spp 18':[],'Spp 19':[],'Spp 20':[],'Spp 21':[],'Spp 22':[],'Spp 23':[],
            'Spp 24': [],'Spp 25':[],'Spp 26':[],'Spp 27':[],'Spp 28':[],'Spp 29':[],'Spp 31':[],'Spp 32':[],'Spp 33':[],'Spp 34':[],'Spp 35':[],'Spp 36':[],
            'Spp 37': [],'Spp 38':[],'Spp 39':[],'Spp 40':[],'Spp 41':[],'Spp 42':[],'Spp 43':[],'Spp 44':[],'Spp 45':[],'Spp 46':[],'Spp 47':[],'Spp 48':[],
        }

        data = pd.DataFrame(mydataCsv)

        if path:
            data.to_csv(path, index=False)
        else:
            data.to_csv('../file/Spp Mahasiswa.csv', index=False)

        messagebox.showinfo("Info", "Lembar kerja tidak ditemukan\nberhasil membuat lembar kerja baru")




class pandas():
    def __init__(self):
        self.path = 'file/Spp Mahasiswa.csv'
        self.mydatafile = pd.read_csv(self.path)

    def Create(self,nama,nim,jurusan):
        tambahsiswa = {
            'Nim': nim,
            'Nama': nama,
            'Jurusan': jurusan,
            'Spp1': '~', 'Spp2':'~', 'Spp3':'~', 'Spp4': '~', 'Spp5':'~', 'Spp6':'~',
            'Spp7': '~', 'Spp8':'~', 'Spp9': '~', 'Spp10':'~', 'Spp11':'~','Spp12': '~',
            'Spp13':'~', 'Spp14':'~', 'Spp15': '~', 'Spp16':'~', 'Spp17':'~', 'Spp18': '~',
            'Spp19':'~', 'Spp20':'~', 'Spp21': '~', 'Spp22':'~', 'Spp23':'~', 'Spp24': '~',
            'Spp25':'~', 'Spp26':'~', 'Spp27': '~', 'Spp28':'~', 'Spp29':'~', 'Spp30': '~',
            'Spp31':'~', 'Spp32':'~', 'Spp33': '~', 'Spp34':'~', 'Spp35':'~', 'Spp36': '~',
            'Spp37':'~', 'Spp38':'~', 'Spp39': '~', 'Spp40':'~', 'Spp41':'~', 'Spp42': '~',
            'Spp43':'~', 'Spp44':'~', 'Spp45': '~', 'Spp46':'~', 'Spp47':'~', 'Spp48': '~'
        }

        self.mydatafile = self.mydatafile.append(tambahsiswa, ignore_index=True)
        self.mydatafile.to_csv(str(self.path), index=False)

    def Delete(self, nama):
        siswa = self.mydatafile[((self.mydatafile.Nama == nama))].index
        self.mydatafile.drop(siswa, inplace=True)
        self.mydatafile.to_csv(str(self.path), index=False)

    def Sorting(self,sortby):
        data = self.mydatafile.sort_values(str(sortby))
        data.to_csv(str(self.path), index=False)

    def UbahMhs(self,nama,namaUbah,nimUbah,jurusanUbah):
        self.mydatafile = pd.read_csv(self.path)
        self.mydatafile.loc[(self.mydatafile['Nama'] == str(nama)), str('Nim')] = nimUbah
        self.mydatafile.loc[(self.mydatafile['Nama'] == str(nama)), str('Jurusan')] = jurusanUbah
        self.mydatafile.loc[(self.mydatafile['Nama'] == str(nama)), str('Nama')] = namaUbah
        self.mydatafile.to_csv(str(self.path), index=False)

    def Filter(self,listName):
        path = 'file/filter.csv'
        self.mydatafile = pd.read_csv(self.path)
        filtering = self.mydatafile[self.mydatafile['Nama'].isin(listName)]
        filtering.to_csv(path, index=False)

    def getSpp(self,name,spp):
        Spp = self.mydatafile[self.mydatafile['Nama'] == name]
        getPosSpp = Spp.iloc[0,:].apply(str).values
        result = getPosSpp[spp + 2]

        return result

    def Pembayaran(self,name,sppPos, spp):
        self.mydatafile = pd.read_csv(self.path)
        self.mydatafile.loc[(self.mydatafile['Nama'] == str(name)), str(sppPos)] = spp
        self.mydatafile.to_csv(str(self.path), index=False)
