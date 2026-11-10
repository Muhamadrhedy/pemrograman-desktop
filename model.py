import re
from dataclasses import dataclass
from datetime import datetime

BATAS_UANG = 1_000_000_000_000

def teks(value, label, batas):
    hasil = str(value).strip()
    if not hasil or len(hasil) > batas:
        raise ValueError(f"{label} wajib diisi, maksimal {batas} karakter.")
    return hasil

def angka(value, label, maksimum=BATAS_UANG):
    raw = str(value).strip()
    if not re.fullmatch(r"[0-9]+", raw):
        raise ValueError(f"{label} harus angka bulat tanpa titik/koma, minimal 0.")
    hasil = int(raw)
    if hasil > maksimum:
        raise ValueError(f"{label} maksimal {maksimum}.")
    return hasil

def periode_valid(value):
    if not re.fullmatch(r"[0-9]{4}-(0[1-9]|1[0-2])", value):
        raise ValueError("Periode harus YYYY-MM, misalnya 2026-10.")
    try:
        datetime.strptime(value, "%Y-%m")
    except ValueError as exc:
        raise ValueError("Periode tidak valid.") from exc
    return value

def rupiah(value):
    return "Rp " + f"{int(value):,}".replace(",", ".")

@dataclass(frozen=True)
class Karyawan:
    nik: str
    nama: str
    jabatan: str
    gaji_pokok: int
    tunjangan: int
    aktif: int = 1

    @classmethod
    def dari_form(cls, data):
        nik = teks(data["nik"], "Nomor Induk Karyawan", 20)
        if not re.fullmatch(r"[A-Za-z0-9-]+", nik):
            raise ValueError("NIK internal hanya huruf, angka, atau tanda hubung.")
        aktif = angka(data["aktif"], "Status aktif", 1)
        return cls(nik, teks(data["nama"], "Nama", 100),
                   teks(data["jabatan"], "Jabatan", 60),
                   angka(data["gaji_pokok"], "Gaji pokok"),
                   angka(data["tunjangan"], "Tunjangan"), aktif)