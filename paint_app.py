import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog


class PaintApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Paint App - Event Handling Demo")
        self.window.geometry("800x600")
        self.window.minsize(600, 400)

        # Variabel untuk menggambar
        self.last_x = None
        self.last_y = None
        self.pen_color = "black"
        self.pen_size = 2
        self.is_drawing = False

        # Variabel untuk posisi mouse
        self.pos_label = None
        self.position_job = None

        self.buat_interface()
        self.bind_events()

    def buat_interface(self):
        # Toolbar
        toolbar = tk.Frame(
            self.window,
            bg="lightgray",
            height=50
        )
        toolbar.pack(fill=tk.X, side=tk.TOP)
        toolbar.pack_propagate(False)

        # Tombol pilih warna
        btn_color = tk.Button(
            toolbar,
            text="Pilih Warna",
            command=self.pilih_warna,
            bg="lightblue"
        )
        btn_color.pack(side=tk.LEFT, padx=5, pady=5)

        # Label ukuran pen
        tk.Label(
            toolbar,
            text="Ukuran:",
            bg="lightgray"
        ).pack(side=tk.LEFT, padx=5)

        # Slider ukuran pen
        self.size_var = tk.IntVar(value=2)

        size_scale = tk.Scale(
            toolbar,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.size_var,
            command=self.ubah_ukuran,
            bg="lightgray",
            highlightthickness=0,
            length=120
        )
        size_scale.pack(side=tk.LEFT, padx=5)

        # Tombol clear
        btn_clear = tk.Button(
            toolbar,
            text="Clear",
            command=self.clear_canvas,
            bg="red",
            fg="white"
        )
        btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

        # Label informasi
        self.info_label = tk.Label(
            toolbar,
            text=f"Warna: {self.pen_color} | Ukuran: {self.pen_size}",
            bg="lightgray"
        )
        self.info_label.pack(side=tk.RIGHT, padx=10)

        # Canvas untuk menggambar
        self.canvas = tk.Canvas(
            self.window,
            bg="white",
            cursor="pencil"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_label = tk.Label(
            self.window,
            text="Siap menggambar | Ctrl+S: Simpan | Ctrl+N: Canvas Baru",
            anchor="w",
            bd=1,
            relief=tk.SUNKEN
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def bind_events(self):
        """Binding mouse, keyboard, dan window events."""

        # Mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        self.canvas.bind("<Motion>", self.show_position)
        self.canvas.bind("<Leave>", self.hide_position)

        # Keyboard shortcuts
        self.window.bind("<Control-s>", self.save_image)
        self.window.bind("<Control-o>", self.open_image)
        self.window.bind("<Control-n>", self.new_canvas)

        # Window event
        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.on_closing
        )

    def pilih_warna(self):
        """Memilih warna pena."""
        color = colorchooser.askcolor(
            color=self.pen_color,
            title="Pilih Warna Pen"
        )

        if color[1]:
            self.pen_color = color[1]
            self.update_info()

    def ubah_ukuran(self, value):
        """Mengubah ukuran pena."""
        self.pen_size = int(float(value))
        self.update_info()

    def clear_canvas(self):
        """Menghapus semua gambar setelah konfirmasi."""
        if messagebox.askyesno(
            "Konfirmasi",
            "Hapus semua gambar?"
        ):
            self.canvas.delete("all")
            self.status_label.config(
                text="Canvas berhasil dibersihkan."
            )

    def update_info(self):
        """Memperbarui informasi warna dan ukuran pena."""
        self.info_label.config(
            text=f"Warna: {self.pen_color} | Ukuran: {self.pen_size}"
        )

    def start_draw(self, event):
        """Dipanggil saat tombol kiri mouse ditekan."""
        self.last_x = event.x
        self.last_y = event.y
        self.is_drawing = True

        self.status_label.config(text="Sedang menggambar...")

        # Membuat titik jika mouse hanya diklik
        self.canvas.create_oval(
            event.x - self.pen_size / 2,
            event.y - self.pen_size / 2,
            event.x + self.pen_size / 2,
            event.y + self.pen_size / 2,
            fill=self.pen_color,
            outline=self.pen_color
        )

    def draw(self, event):
        """Dipanggil saat mouse digerakkan sambil menekan tombol kiri."""
        if (
            self.is_drawing
            and self.last_x is not None
            and self.last_y is not None
        ):
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                width=self.pen_size,
                fill=self.pen_color,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND,
                smooth=True
            )

            self.last_x = event.x
            self.last_y = event.y

    def stop_draw(self, event):
        """Dipanggil saat tombol kiri mouse dilepas."""
        self.is_drawing = False
        self.last_x = None
        self.last_y = None

        self.status_label.config(text="Selesai menggambar.")

    def show_position(self, event):
        """Menampilkan posisi mouse pada canvas."""
        # Batalkan timer penghapusan label sebelumnya
        if self.position_job is not None:
            self.window.after_cancel(self.position_job)
            self.position_job = None

        # Buat label jika belum ada
        if self.pos_label is None:
            self.pos_label = tk.Label(
                self.window,
                text="",
                bg="yellow",
                fg="black",
                padx=4,
                pady=2
            )

        self.pos_label.config(
            text=f"Posisi: ({event.x}, {event.y})"
        )

        # Pindahkan label ke posisi mouse
        self.pos_label.place(
            x=event.x + 10,
            y=event.y + 10
        )

        # Sembunyikan label setelah 1 detik
        self.position_job = self.window.after(
            1000,
            self.hide_position
        )

    def hide_position(self, event=None):
        """Menyembunyikan label posisi mouse."""
        if self.position_job is not None:
            self.window.after_cancel(self.position_job)
            self.position_job = None

        if self.pos_label is not None:
            self.pos_label.place_forget()

    def save_image(self, event=None):
        """Menyimpan canvas sebagai file PostScript."""
        filename = filedialog.asksaveasfilename(
            title="Simpan Gambar",
            defaultextension=".ps",
            filetypes=[
                ("PostScript files", "*.ps"),
                ("All files", "*.*")
            ]
        )

        if filename:
            try:
                self.canvas.postscript(
                    file=filename,
                    colormode="color"
                )
                messagebox.showinfo(
                    "Berhasil",
                    f"Gambar berhasil disimpan:\n{filename}"
                )
            except tk.TclError as error:
                messagebox.showerror(
                    "Gagal Menyimpan",
                    str(error)
                )

        return "break"

    def open_image(self, event=None):
        """Placeholder untuk fitur membuka gambar."""
        messagebox.showinfo(
            "Informasi",
            "Fitur membuka gambar belum diimplementasikan."
        )
        return "break"

    def new_canvas(self, event=None):
        """Membuat canvas baru dengan menghapus gambar."""
        if messagebox.askyesno(
            "Canvas Baru",
            "Buat canvas baru? Gambar saat ini akan dihapus."
        ):
            self.canvas.delete("all")
            self.status_label.config(
                text="Canvas baru siap digunakan."
            )

        return "break"

    def on_closing(self):
        """Menangani event saat jendela ditutup."""
        if messagebox.askokcancel(
            "Keluar",
            "Yakin ingin keluar? Gambar yang belum disimpan akan hilang."
        ):
            self.window.destroy()

    def jalankan(self):
        """Menjalankan aplikasi Tkinter."""
        self.window.mainloop()


if __name__ == "__main__":
    app = PaintApp()
    app.jalankan()
