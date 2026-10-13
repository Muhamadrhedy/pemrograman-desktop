import tkinter as tk

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Timer Sederhana")
        
        self.sisa_waktu = 10  # 10 detik
        self.timer_id = None
        self.is_running = False

        # Label Tampilan Waktu
        self.lbl_waktu = tk.Label(root, text=f"00:{self.sisa_waktu:02d}", font=("Arial", 28, "bold"))
        self.lbl_waktu.pack(pady=15)

        # Tombol Kontrol
        self.btn_mulai = tk.Button(root, text="Mulai", command=self.mulai_timer)
        self.btn_mulai.pack(pady=5)

        self.btn_stop = tk.Button(root, text="Stop", command=self.stop_timer)
        self.btn_stop.pack(pady=5)

    def mulai_timer(self):
        if not self.is_running:
            self.is_running = True
            self.hitung_mundur()

    def hitung_mundur(self):
        if self.sisa_waktu > 0 and self.is_running:
            self.sisa_waktu -= 1
            self.lbl_waktu.config(text=f"00:{self.sisa_waktu:02d}")
            # Simpan ID timer agar bisa dibatalkan nanti
            self.timer_id = self.root.after(1000, self.hitung_mundur)
        elif self.sisa_waktu == 0:
            self.is_running = False
            self.lbl_waktu.config(text="Waktu Habis!")

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()