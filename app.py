import tkinter as tk
from tkinter import ttk, messagebox
from repository import KaryawanRepository, GajiRepository
from views.karyawan import KaryawanView
from views.gaji import GajiView

class PenggajianApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SiGaji — Penggajian Karyawan")
        self.geometry("1000x650")
        self.buat_tampilan();
        self.dashboard()

    def buat_tampilan(self):
        self.content = ttk.Frame(self,padding=20)
        self.content.pack(fill="both",expand=True)
        bar = tk.Menu(self)
        file = tk.Menu(bar,tearoff=False)
        file.add_command(label="Dashboard",command=self.dashboard)
        file.add_separator();file.add_command(label="Keluar",command=self.keluar)
        bar = tk.Menu(self)
        file = tk.Menu(bar,tearoff=False)
        file.add_command(label="Dashboard",command=self.dashboard)
        file.add_separator();file.add_command(label="Keluar",command=self.keluar)
        bar.add_cascade(label="File",menu=file)
        master = tk.Menu(bar,tearoff=False)
        master.add_command(label="Data Karyawan",command=self.data_karyawan)
        bar.add_cascade(label="Master Data",menu=master)
        transaksi = tk.Menu(bar,tearoff=False)
        transaksi.add_command(label="Proses Gaji",command=self.proses_gaji)
        bar.add_cascade(label="Transaksi",menu=transaksi)
        laporan = tk.Menu(bar,tearoff=False)
        laporan.add_command(label="Riwayat, Slip, dan Rekap",command=lambda:self.placeholder("Laporan"))
        bar.add_cascade(label="Laporan",menu=laporan)
        bantuan = tk.Menu(bar,tearoff=False)
        bantuan.add_command(label="Tentang",command=lambda:messagebox.showinfo("SiGaji","Proyek penggajian desktop Modul 5",parent=self))
        bar.add_cascade(label="Bantuan",menu=bantuan)
        self.config(menu=bar)
        self.protocol("WM_DELETE_WINDOW",self.keluar)


    def bersihkan(self):
        for child in self.content.winfo_children():child.destroy()

    def placeholder(self,nama):
        self.bersihkan()
        ttk.Label(self.content,text=nama,font=("Arial",18,"bold")).pack(anchor="w")
        ttk.Label(self.content,text="Fitur akan dibangun pada tahap berikutnya.").pack(anchor="w",pady=10)

    
    def data_karyawan(self):
        self.bersihkan()
        KaryawanView(self.content,KaryawanRepository()).pack(fill="both",expand=True)

    def proses_gaji(self):
        self.bersihkan()
        GajiView(self.content,KaryawanRepository(),GajiRepository()).pack(fill="both",expand=True)

    def dashboard(self):self.placeholder("Dashboard Penggajian")

    def keluar(self):
        if messagebox.askyesno("Keluar","Tutup aplikasi?",parent=self):self.destroy()

if __name__ == "__main__":PenggajianApp().mainloop()