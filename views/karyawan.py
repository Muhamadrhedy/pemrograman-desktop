import tkinter as tk
from tkinter import ttk, messagebox
from model import Karyawan, rupiah
from ui_common import aman, tabel, input_teks

class KaryawanView(ttk.Frame):
    def __init__(self, parent, repo):
        super().__init__(parent,padding=15)
        self.repo = repo
        self.rows = {}
        ttk.Label(self,text="Data Karyawan",font=("Arial",16,"bold")).pack(anchor="w")
        bar = ttk.Frame(self);bar.pack(fill="x",pady=8)
        self.cari = tk.StringVar()
        ttk.Entry(bar,textvariable=self.cari).pack(side="left")
        for label, aksi in [("Cari / Muat Ulang",self.muat),("Tambah",lambda:self.form()),
                             ("Edit",self.edit),("Hapus",self.hapus)]:
            ttk.Button(bar,text=label,command=aksi).pack(side="left",padx=4)
        self.tree = tabel(self,dict(nik="NIK internal",nama="Nama",jabatan="Jabatan",gaji_pokok="Gaji Pokok",tunjangan="Tunjangan",aktif="Aktif"))
        self.tree.bind("<Double-1>",lambda event:self.edit())
        self.muat()

    def muat(self):
        def proses():
            rows = self.repo.semua(self.cari.get().strip())
            self.tree.delete(*self.tree.get_children())
            self.rows = {str(r["id"]):r for r in rows}
            for key,r in self.rows.items():
                self.tree.insert("","end",iid=key,values=(r["nik"],r["nama"],r["jabatan"],rupiah(r["gaji_pokok"]),rupiah(r["tunjangan"]),"Ya" if r["aktif"] else "Tidak"))
        aman(self,proses)

    def dipilih(self):
        keys = self.tree.selection()
        if not keys:
            raise ValueError("Pilih satu karyawan pada tabel.")
        return self.rows[keys[0]]

    def edit(self):
        aman(self,lambda:self.form(self.dipilih()))

    def form(self, row=None):
        row = row or {}
        window = tk.Toplevel(self);window.title("Edit Karyawan" if row else "Tambah Karyawan")
        window.transient(self.winfo_toplevel());window.grab_set()
        frame = ttk.Frame(window,padding=15);frame.pack(fill="both",expand=True)
        fields = {}
        for i,(key,label) in enumerate([("nik","NIK internal"),("nama","Nama"),("jabatan","Jabatan"),
                                        ("gaji_pokok","Gaji pokok (rupiah bulat)"),("tunjangan","Tunjangan (rupiah bulat)")]):
            fields[key] = input_teks(frame,label,i,str(row.get(key,"0" if key in ("gaji_pokok","tunjangan") else "")))
        aktif = tk.IntVar(value=row.get("aktif",1))
        ttk.Checkbutton(frame,text="Karyawan aktif",variable=aktif).grid(row=5,column=1,sticky="w")
        def simpan():
            def proses():
                data = {key:var.get() for key,var in fields.items()}
                data["aktif"] = aktif.get()
                self.repo.simpan(Karyawan.dari_form(data),row.get("id"))
                window.destroy();self.muat()
            aman(window,proses)
        ttk.Button(frame,text="Simpan",command=simpan).grid(row=6,column=0,pady=10)
        ttk.Button(frame,text="Batal",command=window.destroy).grid(row=6,column=1)

    def hapus(self):
        def proses():
            row = self.dipilih()
            if messagebox.askyesno("Konfirmasi",f"Hapus {row['nama']}?",parent=self):
                self.repo.hapus(row["id"]);self.muat()
        aman(self,proses)