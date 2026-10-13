import tkinter as tk

def jalankan_terus():
    print("Fungsi dipanggil setiap 1 detik")
    # Panggil ulang fungsi ini setelah 1000 milidetik (1 detik)
    root.after(1000, jalankan_terus)

if __name__ == "__main__":
    # Inisialisasi jendela utama Tkinter
    root = tk.Tk()
    root.title("Contoh Looping root.after()")
    root.geometry("300x200")

    # Label informasi untuk pengguna
    lbl_info = tk.Label(root, text="Cek output di Terminal/Console!", font=("Arial", 10))
    lbl_info.pack(expand=True)

    # Memulai pemanggilan pertama setelah jendela siap
    root.after(1000, jalankan_terus)

    # Menjalankan event loop utama aplikasi GUI
    root.mainloop()