import tkinter as tkinter

class AnimasiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animasi Bola Memantul")

        # Buat Canvas
        self.canvas = tkinter.Canvas(root, width=400, height=200, bg="white")
        self.canvas.pack(padx=10, pady=10)

        # Buat objek lingkaran (oval) pada koordinat awal
        self.bola = self.canvas.create_oval(10, 80, 40, 110, fill="blue")
        self.dx = 3  # Kecepatan gerak sumbu X

        # Jalankan animasi
        self.gerakkan_bola()

    def gerakkan_bola(self):
        # Geser objek sejauh dx
        self.canvas.move(self.bola, self.dx, 0)
        
        # Ambil koordinat posisi bola saat ini
        posisi = self.canvas.coords(self.bola)
        
        # BatMemantul jika menabrak dinding kanan atau kiri canvas (lebar 400)
        if posisi[2] >= 400 or posisi[0] <= 0:
            self.dx = -self.dx

        # Perbarui frame setiap 20 milidetik (sekitar 50 FPS)
        self.root.after(20, self.gerakkan_bola)

if __name__ == "__main__":
    root = tkinter.Tk()
    app = AnimasiApp(root)
    root.mainloop()