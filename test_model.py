import unittest
from model import hitung_gaji, Karyawan, periode_valid

class TestPenggajian(unittest.TestCase):
    def test_hitung(self):
        h = hitung_gaji(5000000,500000,10,25000,100000)
        self.assertEqual(h["uang_lembur"],250000)
        self.assertEqual(h["bruto"],5750000)
        self.assertEqual(h["netto"],5650000)
    def test_nol(self):
        self.assertEqual(hitung_gaji(0,0,0,0,0)["netto"],0)
    def test_input_gagal(self):
        for jam in ("abc","-1","1.5","201"):
            with self.subTest(jam=jam),self.assertRaises(ValueError):hitung_gaji(100,0,jam,1,0)
        with self.assertRaises(ValueError):hitung_gaji(100,0,0,0,101)
    def test_periode(self):
        self.assertEqual(periode_valid("2026-10"),"2026-10")
        for p in ("2026-13","26-10","0000-01"):
            with self.assertRaises(ValueError):periode_valid(p)
    def test_model(self):
        m = Karyawan.dari_form(dict(nik="001",nama=" Budi ",jabatan="Staf",gaji_pokok="100",tunjangan="0",aktif="1"))
        self.assertEqual(m.nik,"001");self.assertEqual(m.nama,"Budi")

if __name__ == "__main__":unittest.main()