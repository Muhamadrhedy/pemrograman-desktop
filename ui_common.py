import logging
import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error

logging.basicConfig(filename="penggajian.log",level=logging.ERROR,
                    format="%(asctime)s %(levelname)s %(message)s")

def aman(parent, aksi):
    try:
        return aksi()
    except ValueError as exc:
        messagebox.showwarning("Periksa data", str(exc), parent=parent)
    except Error:
        logging.exception("Operasi database gagal")
        messagebox.showerror("Database", "Koneksi/operasi MySQL gagal. Periksa server, config.ini, schema, dan penggajian.log.", parent=parent)
    except Exception:
        logging.exception("Operasi aplikasi gagal")
        messagebox.showerror("Kesalahan", "Proses gagal. Periksa penggajian.log.", parent=parent)

def tabel(parent, kolom):
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, pady=10)
    tree = ttk.Treeview(frame, columns=tuple(kolom), show="headings", selectmode="browse")
    for key, label in kolom.items():
        tree.heading(key,text=label)
        tree.column(key,width=135,minwidth=80)
    vert = ttk.Scrollbar(frame,orient="vertical",command=tree.yview)
    horiz = ttk.Scrollbar(frame,orient="horizontal",command=tree.xview)
    tree.configure(yscrollcommand=vert.set,xscrollcommand=horiz.set)
    tree.grid(row=0,column=0,sticky="nsew")
    vert.grid(row=0,column=1,sticky="ns")
    horiz.grid(row=1,column=0,sticky="ew")
    frame.rowconfigure(0,weight=1);frame.columnconfigure(0,weight=1)
    return tree

def input_teks(parent, label, row, awal=""):
    ttk.Label(parent,text=label).grid(row=row,column=0,sticky="w",padx=5,pady=4)
    value = tk.StringVar(value=awal)
    ttk.Entry(parent,textvariable=value,width=35).grid(row=row,column=1,sticky="ew",padx=5,pady=4)
    return value