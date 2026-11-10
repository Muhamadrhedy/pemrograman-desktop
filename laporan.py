import csv
from model import rupiah

def isi_slip(r):
    lines = ["SLIP GAJI — SIMULASI PRAKTIKUM",f"ID: {r['id']} | Periode: {r['periode']}",
             f"NIK: {r['nik']}",f"Nama: {r['nama']}",f"Jabatan: {r['jabatan']}",
             f"Lembur: {r['jam_lembur']} jam x {rupiah(r['tarif_lembur'])}"]
    for key,label in [("gaji_pokok","Gaji pokok"),("tunjangan","Tunjangan"),("uang_lembur","Uang lembur"),
                      ("bruto","Bruto"),("potongan","Potongan"),("netto","Gaji bersih")]:
        lines.append(f"{label}: {rupiah(r[key])}")
    return "\n".join(lines) + "\n"

def sel_aman(value):
    raw = str(value)
    return "'" + raw if raw.lstrip().startswith(("=","+","-","@")) else raw

def ekspor_csv(path, rows):
    keys = ["periode","nik","nama","jabatan","gaji_pokok","tunjangan","jam_lembur","tarif_lembur","uang_lembur","potongan","bruto","netto"]
    with open(path,"w",newline="",encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(keys)
        for r in rows:
            writer.writerow([sel_aman(r[key]) for key in keys])