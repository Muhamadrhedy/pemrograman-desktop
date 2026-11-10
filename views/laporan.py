from datetime import date
from pathlib import Path
from tkinter import ttk, StringVar, filedialog
from model import rupiah
from laporan import isi_slip, ekspor_csv
from ui_common import aman, tabel

class LaporanView(ttk.Frame):
    def __init__(self,parent,repo):
        super().__init__(parent,padding=15)
        self.repo = repo;self.rows = {};self.periode_data = ""
        ttk.Label(self,text="Riwayat Gaji dan Laporan",font=("Arial",16,"bold")).pack(anchor="w")
        bar = ttk.Frame(self);bar.pack(fill="x",pady=10)
        ttk.Label(bar,text="Periode YYYY-MM").pack(side="left")
        self.periode = StringVar(value=date.today().strftime("%Y-%m"))
        ttk.Entry(bar,textvariable=self.periode,width=10).pack(side="left",padx=6)
        for label,aksi in [("Tampilkan",self.muat),("Simpan Slip TXT",self.slip),("Ekspor CSV",self.csv)]:
            ttk.Button(bar,text=label,command=aksi).pack(side="left",padx=4)
        self.tree = tabel(self,dict(nik="NIK",nama="Nama",jabatan="Jabatan",bruto="Bruto",potongan="Potongan",netto="Netto"))
        self.info = StringVar()
        ttk.Label(self,textvariable=self.info).pack(anchor="w")
        self.muat()

    def muat(self):
        def proses():
            periode = self.periode.get().strip()
            rows = self.repo.semua(periode)
            self.tree.delete(*self.tree.get_children())
            self.rows = {str(r["id"]):r for r in rows};self.periode_data = periode
            for key,r in self.rows.items():
                self.tree.insert("","end",iid=key,values=(r["nik"],r["nama"],r["jabatan"],rupiah(r["bruto"]),rupiah(r["potongan"]),rupiah(r["netto"])))
            self.info.set(f"Periode ditampilkan: {periode}; {len(rows)} slip; total netto {rupiah(sum(r['netto'] for r in rows))}")
        aman(self,proses)

    def validasi_tampilan(self):
        if self.periode_data != self.periode.get().strip():
            raise ValueError("Periode berubah. Klik Tampilkan dahulu sebelum mengekspor.")

    def slip(self):
        def proses():
            self.validasi_tampilan()
            keys = self.tree.selection()
            if not keys:raise ValueError("Pilih satu slip pada tabel.")
            r = self.rows[keys[0]]
            path = filedialog.asksaveasfilename(parent=self,title="Simpan Slip",defaultextension=".txt",initialfile=f"slip_{r['id']}_{r['periode']}.txt",filetypes=[("Teks","*.txt")])
            if path:Path(path).write_text(isi_slip(r),encoding="utf-8")
        aman(self,proses)

    def csv(self):
        def proses():
            self.validasi_tampilan()
            if not self.rows:raise ValueError("Tidak ada data untuk diekspor.")
            path = filedialog.asksaveasfilename(parent=self,defaultextension=".csv",initialfile=f"gaji_{self.periode_data}.csv",filetypes=[("CSV","*.csv")])
            if path:ekspor_csv(path,list(self.rows.values()))
        aman(self,proses)