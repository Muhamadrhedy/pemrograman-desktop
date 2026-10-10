import tkinter as tk


class KonverterSuhu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Konverter Suhu - State Management Demo")
        self.window.geometry("500x560")
        self.window.configure(bg="lightblue")
        self.window.resizable(False, False)

        # Variabel kontrol untuk setiap skala suhu
        # StringVar memungkinkan input diketik secara bertahap
        self.celsius_var = tk.StringVar(value="0")
        self.fahrenheit_var = tk.StringVar(value="32")
        self.kelvin_var = tk.StringVar(value="273.15")
        self.rankine_var = tk.StringVar(value="491.67")

        # Mencegah trace memanggil konversi berulang
        self.updating = False

        self.buat_interface()
        self.setup_traces()
        self.update_info()

    def buat_interface(self):
        # Judul aplikasi
        title_label = tk.Label(
            self.window,
            text="KONVERTER SUHU UNIVERSAL",
            font=("Arial", 16, "bold"),
            bg="lightblue"
        )
        title_label.pack(pady=20)

        # Frame utama
        main_frame = tk.Frame(
            self.window,
            bg="lightblue"
        )
        main_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20
        )

        # Celsius
        self.buat_input(
            main_frame,
            "Celsius (°C):",
            self.celsius_var
        )

        # Fahrenheit
        self.buat_input(
            main_frame,
            "Fahrenheit (°F):",
            self.fahrenheit_var
        )

        # Kelvin
        self.buat_input(
            main_frame,
            "Kelvin (K):",
            self.kelvin_var
        )

        # Rankine
        self.buat_input(
            main_frame,
            "Rankine (°R):",
            self.rankine_var
        )

        # Tombol reset
        btn_reset = tk.Button(
            main_frame,
            text="Reset Semua",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            command=self.reset_all
        )
        btn_reset.pack(pady=15)

        # Frame informasi suhu
        info_frame = tk.Frame(
            main_frame,
            bg="lightyellow",
            relief=tk.GROOVE,
            bd=2
        )
        info_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            info_frame,
            text="INFORMASI SUHU",
            font=("Arial", 12, "bold"),
            bg="lightyellow"
        ).pack(pady=5)

        self.info_label = tk.Label(
            info_frame,
            text="Masukkan nilai suhu di salah satu field",
            font=("Arial", 10),
            bg="lightyellow",
            justify=tk.LEFT,
            wraplength=400
        )
        self.info_label.pack(padx=10, pady=8)

    def buat_input(self, parent, label_text, variable):
        """Membuat satu baris input suhu."""
        frame = tk.Frame(
            parent,
            bg="white",
            relief=tk.RAISED,
            bd=2
        )
        frame.pack(fill=tk.X, pady=5)

        tk.Label(
            frame,
            text=label_text,
            font=("Arial", 12, "bold"),
            bg="white",
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        entry = tk.Entry(
            frame,
            textvariable=variable,
            font=("Arial", 12),
            width=20,
            justify="center"
        )
        entry.pack(side=tk.RIGHT, padx=10, pady=10)

    def setup_traces(self):
        """Memantau perubahan pada setiap variabel."""
        self.celsius_var.trace_add(
            "write", self.from_celsius
        )
        self.fahrenheit_var.trace_add(
            "write", self.from_fahrenheit
        )
        self.kelvin_var.trace_add(
            "write", self.from_kelvin
        )
        self.rankine_var.trace_add(
            "write", self.from_rankine
        )

    def konversi(self, sumber, nilai):
        """Mengubah nilai sumber ke tiga skala suhu lainnya."""
        if self.updating:
            return

        try:
            nilai = float(nilai)
        except (ValueError, TypeError):
            self.info_label.config(
                text="Masukkan angka yang valid."
            )
            return

        # Konversi nilai sumber menjadi Celsius
        if sumber == "celsius":
            celsius = nilai
        elif sumber == "fahrenheit":
            celsius = (nilai - 32) * 5 / 9
        elif sumber == "kelvin":
            celsius = nilai - 273.15
        else:  # Rankine
            celsius = (nilai * 5 / 9) - 273.15

        # Hitung semua skala berdasarkan Celsius
        fahrenheit = (celsius * 9 / 5) + 32
        kelvin = celsius + 273.15
        rankine = kelvin * 9 / 5

        self.updating = True
        try:
            # Jangan menimpa field yang sedang diedit
            if sumber != "celsius":
                self.celsius_var.set(
                    self.format_angka(celsius)
                )

            if sumber != "fahrenheit":
                self.fahrenheit_var.set(
                    self.format_angka(fahrenheit)
                )

            if sumber != "kelvin":
                self.kelvin_var.set(
                    self.format_angka(kelvin)
                )

            if sumber != "rankine":
                self.rankine_var.set(
                    self.format_angka(rankine)
                )
        finally:
            self.updating = False

        self.update_info(celsius)

    def format_angka(self, angka):
        """Membatasi tampilan hingga dua angka desimal."""
        return f"{angka:.2f}".rstrip("0").rstrip(".")

    # Callback untuk setiap variabel

    def from_celsius(self, *args):
        """Konversi dari Celsius."""
        self.konversi(
            "celsius", self.celsius_var.get()
        )

    def from_fahrenheit(self, *args):
        """Konversi dari Fahrenheit."""
        self.konversi(
            "fahrenheit", self.fahrenheit_var.get()
        )

    def from_kelvin(self, *args):
        """Konversi dari Kelvin."""
        self.konversi(
            "kelvin", self.kelvin_var.get()
        )

    def from_rankine(self, *args):
        """Konversi dari Rankine."""
        self.konversi(
            "rankine", self.rankine_var.get()
        )

    def reset_all(self):
        """Mengembalikan semua skala ke 0°C."""
        self.updating = True
        try:
            self.celsius_var.set("0")
            self.fahrenheit_var.set("32")
            self.kelvin_var.set("273.15")
            self.rankine_var.set("491.67")
        finally:
            self.updating = False

        self.update_info(0)

    def update_info(self, celsius=None):
        """Memperbarui informasi berdasarkan suhu Celsius."""
        if celsius is None:
            try:
                celsius = float(self.celsius_var.get())
            except (ValueError, TypeError):
                self.info_label.config(
                    text="Masukkan nilai suhu yang valid."
                )
                return

        info_text = f"Suhu saat ini: {celsius:.2f}°C\n"

        if abs(celsius) < 0.005:
            info_text += "Titik beku air (kondisi normal)"
        elif abs(celsius - 100) < 0.005:
            info_text += "Titik didih air (kondisi normal)"
        elif abs(celsius + 273.15) < 0.005:
            info_text += "Suhu nol absolut"
        elif celsius < 0:
            info_text += "Di bawah titik beku air"
        elif celsius > 100:
            info_text += "Di atas titik didih air"
        else:
            info_text += "Suhu di antara 0°C dan 100°C"

        self.info_label.config(text=info_text)

    def jalankan(self):
        """Menjalankan aplikasi."""
        self.window.mainloop()


if __name__ == "__main__":
    app = KonverterSuhu()
    app.jalankan()
