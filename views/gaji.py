from datetime import date
from tkinter import ttk, StringVar
from model import hitung_gaji, periode_valid, rupiah
from ui_common import aman, input_teks

class GajiView(ttk.Frame):
    def __init__(self,parent,karyawan_repo,gaji_repo):
        super().__init__(parent,padding=15)
        self.karyawan_repo = karyawan_repo;self.gaji_repo = gaji_repo
        self.rows = {}
        ttk.Label(self,text="Proses Penggajian",font=("Arial",16,"bold")).pack(anchor="w")
        frame = ttk.Frame(self);frame.pack(anchor="w",fill="x",pady=10)
        ttk.Label(frame,text="Karyawan aktif").grid(row=0,column=0,sticky="w")
        self.pilihan = StringVar()
        self.combo = ttk.Combobox(frame,textvariable=self.pilihan,state="readonly",width=45)
        self.combo.grid(row=0,column=1,sticky="ew")
        self.periode = input_teks(frame,"Periode YYYY-MM",1,date.today().strftime("%Y-%m"))
        self.jam = input_teks(frame,"Jam lembur (0–200)",2,"0")
        self.tarif = input_teks(frame,"Tarif per jam (rupiah bulat)",3,"25000")
        self.potongan = input_teks(frame,"Potongan (rupiah bulat)",4,"0")
        ttk.Button(frame,text="Pratinjau Hitungan",command=self.preview).grid(row=5,column=0,pady=10)
        ttk.Button(frame,text="Simpan Gaji",command=self.simpan).grid(row=5,column=1,pady=10)
        self.hasil = StringVar(value="Pilih karyawan, isi komponen, lalu lihat pratinjau.")
        ttk.Label(self,textvariable=self.hasil,wraplength=750).pack(anchor="w",pady=15)
        ttk.Label(self,text="Satu gaji per karyawan per periode. Nilai final dihitung ulang saat simpan dari data master terkini.").pack(anchor="w")
        aman(self,self.muat)

    def muat(self):
        rows = self.karyawan_repo.semua(hanya_aktif=True)
        self.rows = {f"{r['id']} | {r['nik']} — {r['nama']}":r for r in rows}
        self.combo["values"] = list(self.rows)
        if self.rows:self.combo.current(0)
        else:self.hasil.set("Belum ada karyawan aktif. Tambahkan melalui menu Data Karyawan.")

    def data(self):
        if self.pilihan.get() not in self.rows:
            raise ValueError("Pilih karyawan aktif.")
        return self.rows[self.pilihan.get()]

    def preview(self):
        def proses():
            row = self.data();periode_valid(self.periode.get().strip())
            h = hitung_gaji(row["gaji_pokok"],row["tunjangan"],self.jam.get(),self.tarif.get(),self.potongan.get())
            self.hasil.set(f"Pratinjau {row['nama']}: bruto {rupiah(h['bruto'])}; potongan {rupiah(h['potongan'])}; netto {rupiah(h['netto'])}. Belum tersimpan.")
        aman(self,proses)

    def simpan(self):
        def proses():
            row = self.data()
            id_gaji = self.gaji_repo.simpan(row["id"],self.periode.get().strip(),self.jam.get(),self.tarif.get(),self.potongan.get())
            self.hasil.set(f"Gaji tersimpan dengan ID {id_gaji}. Buka menu Laporan untuk melihat hasil final dan slip.")
        aman(self,proses)