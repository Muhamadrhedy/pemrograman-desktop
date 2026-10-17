import tkinter as tk
from tkinter import messagebox, ttk
import re
from datetime import datetime


class RegistrasiApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Form Registrasi - Validasi Demo")
        self.window.geometry("650x760")
        self.window.minsize(600, 700)
        self.window.configure(bg="#eef2f7")

        # Variabel kontrol
        self.nama_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        # StringVar agar input umur yang belum valid tidak langsung memicu error Tcl.
        self.age_var = tk.StringVar(value="18")
        self.gender_var = tk.StringVar(value="Pria")
        self.agree_var = tk.BooleanVar(value=False)

        self.validation_status = {
            "nama": False,
            "email": False,
            "phone": False,
            "password": False,
            "confirm_password": False,
            "age": False,
            "agree": False,
        }
        self.is_loading = False

        self.buat_interface()
        self.setup_validation()
        self.update_submit_button()

    def buat_interface(self):
        # Header
        header = tk.Frame(self.window, bg="#173b67", height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="FORM REGISTRASI PENGGUNA",
            font=("Arial", 18, "bold"),
            bg="#173b67",
            fg="white",
        ).pack(pady=(22, 4))

        tk.Label(
            header,
            text="Lengkapi data berikut dengan benar",
            font=("Arial", 10),
            bg="#173b67",
            fg="#dce8f7",
        ).pack()

        # Area form dengan scrollbar
        container = tk.Frame(self.window, bg="#eef2f7")
        container.pack(fill=tk.BOTH, expand=True, padx=18, pady=14)

        canvas = tk.Canvas(container, bg="#eef2f7", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.main_frame = tk.Frame(canvas, bg="#eef2f7")

        self.main_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas_window = canvas.create_window(
            (0, 0), window=self.main_frame, anchor="nw"
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        def resize_inner(event):
            canvas.itemconfigure(canvas_window, width=event.width)

        canvas.bind("<Configure>", resize_inner)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Input fields
        self.buat_input_field(
            self.main_frame, "Nama Lengkap:", self.nama_var,
            "nama", "Minimal 3 karakter; hanya huruf dan spasi"
        )
        self.buat_input_field(
            self.main_frame, "Email:", self.email_var,
            "email", "Contoh: nama@domain.com"
        )
        self.buat_input_field(
            self.main_frame, "Nomor Telepon:", self.phone_var,
            "phone", "Format Indonesia: 08xxxxxxxxxx (10–13 digit)"
        )
        self.buat_input_field(
            self.main_frame, "Password:", self.password_var,
            "password", "Minimal 8 karakter, kombinasi huruf dan angka", show="*"
        )
        self.buat_input_field(
            self.main_frame, "Konfirmasi Password:", self.confirm_password_var,
            "confirm_password", "Harus sama dengan password", show="*"
        )

        # Umur
        age_frame = tk.Frame(self.main_frame, bg="#eef2f7")
        age_frame.pack(fill=tk.X, pady=(12, 2))
        tk.Label(
            age_frame, text="Umur:", font=("Arial", 11, "bold"),
            bg="#eef2f7", width=22, anchor="w"
        ).pack(side=tk.LEFT)

        self.age_spinbox = tk.Spinbox(
            age_frame, from_=13, to=100, textvariable=self.age_var,
            font=("Arial", 11), width=10
        )
        self.age_spinbox.pack(side=tk.LEFT, padx=5)

        self.age_indicator = tk.Label(
            age_frame, text="●", font=("Arial", 15),
            fg="#dc2626", bg="#eef2f7"
        )
        self.age_indicator.pack(side=tk.LEFT, padx=5)

        self.age_hint = tk.Label(
            self.main_frame, text="Umur minimal 13 tahun dan maksimal 100 tahun",
            font=("Arial", 9), fg="#64748b", bg="#eef2f7", anchor="w"
        )
        self.age_hint.pack(fill=tk.X, padx=(25, 0))

        # Jenis kelamin
        gender_frame = tk.Frame(self.main_frame, bg="#eef2f7")
        gender_frame.pack(fill=tk.X, pady=(14, 8))
        tk.Label(
            gender_frame, text="Jenis Kelamin:", font=("Arial", 11, "bold"),
            bg="#eef2f7", width=22, anchor="w"
        ).pack(side=tk.LEFT)

        radio_frame = tk.Frame(gender_frame, bg="#eef2f7")
        radio_frame.pack(side=tk.LEFT)
        for gender in ("Pria", "Wanita"):
            tk.Radiobutton(
                radio_frame, text=gender, variable=self.gender_var, value=gender,
                bg="#eef2f7", activebackground="#eef2f7",
                font=("Arial", 10), selectcolor="white"
            ).pack(side=tk.LEFT, padx=(0, 12))

        # Persetujuan
        self.agree_checkbox = tk.Checkbutton(
            self.main_frame,
            text="Saya menyetujui syarat dan ketentuan yang berlaku",
            variable=self.agree_var,
            font=("Arial", 10),
            bg="#eef2f7",
            activebackground="#eef2f7",
            command=self.validate_agreement,
        )
        self.agree_checkbox.pack(anchor="w", pady=(12, 14))

        # Progress
        progress_frame = tk.Frame(
            self.main_frame, bg="white", padx=12, pady=10,
            highlightbackground="#d6deea", highlightthickness=1
        )
        progress_frame.pack(fill=tk.X, pady=(2, 12))

        tk.Label(
            progress_frame, text="Kelengkapan Form",
            font=("Arial", 10, "bold"), bg="white", fg="#1e293b"
        ).pack(anchor="w")

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var,
            maximum=100, mode="determinate"
        )
        self.progress_bar.pack(fill=tk.X, pady=7)

        self.progress_label = tk.Label(
            progress_frame, text="0% Complete (0/7 fields)",
            font=("Arial", 9), bg="white", fg="#475569"
        )
        self.progress_label.pack(anchor="w")

        self.submit_btn = tk.Button(
            self.main_frame, text="DAFTAR SEKARANG",
            font=("Arial", 12, "bold"), bg="#94a3b8", fg="white",
            activebackground="#15803d", activeforeground="white",
            relief=tk.FLAT, cursor="hand2", height=2,
            state=tk.DISABLED, command=self.submit_form
        )
        self.submit_btn.pack(fill=tk.X, pady=(2, 12))

        tk.Label(
            self.main_frame,
            text="Demo validasi form — data tidak dikirim ke server.",
            font=("Arial", 9), fg="#64748b", bg="#eef2f7"
        ).pack(pady=(0, 8))

    def buat_input_field(self, parent, label_text, variable, field_name, hint_text, show=None):
        """Membuat input field dengan indikator validasi visual."""
        field_frame = tk.Frame(parent, bg="#eef2f7")
        field_frame.pack(fill=tk.X, pady=(7, 1))

        tk.Label(
            field_frame, text=label_text, font=("Arial", 10, "bold"),
            bg="#eef2f7", fg="#1e293b", width=22, anchor="w"
        ).pack(side=tk.LEFT)

        entry_frame = tk.Frame(field_frame, bg="#eef2f7")
        entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        entry = tk.Entry(
            entry_frame, textvariable=variable, font=("Arial", 10),
            show=show, relief=tk.SOLID, bd=1
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)

        indicator = tk.Label(
            entry_frame, text="●", font=("Arial", 15),
            fg="#dc2626", bg="#eef2f7"
        )
        indicator.pack(side=tk.LEFT, padx=(7, 2))

        hint_label = tk.Label(
            parent, text=hint_text, font=("Arial", 9),
            fg="#64748b", bg="#eef2f7", anchor="w"
        )
        hint_label.pack(fill=tk.X, padx=(25, 0))

        setattr(self, f"{field_name}_indicator", indicator)
        setattr(self, f"{field_name}_entry", entry)
        setattr(self, f"{field_name}_hint", hint_label)

    def setup_validation(self):
        """Menghubungkan perubahan input dengan validasi real-time."""
        self.nama_var.trace_add("write", lambda *_: self.validate_nama())
        self.email_var.trace_add("write", lambda *_: self.validate_email())
        self.phone_var.trace_add("write", lambda *_: self.validate_phone())
        self.password_var.trace_add("write", lambda *_: self.validate_password())
        self.confirm_password_var.trace_add(
            "write", lambda *_: self.validate_confirm_password()
        )
        self.age_var.trace_add("write", lambda *_: self.validate_age())

    def set_validation_status(self, field_name, is_valid, message):
        """Memperbarui status, indikator, dan teks bantuan field."""
        self.validation_status[field_name] = is_valid
        indicator = getattr(self, f"{field_name}_indicator")
        hint_label = getattr(self, f"{field_name}_hint")

        if is_valid:
            indicator.config(fg="#16a34a")
            hint_label.config(fg="#15803d", text=f"✓ {message}")
        else:
            indicator.config(fg="#dc2626")
            hint_label.config(fg="#dc2626", text=f"✗ {message}")

        self.update_submit_button()

    def validate_nama(self):
        nama = self.nama_var.get().strip()
        if len(nama) < 3:
            self.set_validation_status("nama", False, "Nama minimal 3 karakter")
            return False
        if not re.fullmatch(r"[a-zA-ZÀ-ÿ\s]+", nama):
            self.set_validation_status("nama", False, "Gunakan huruf dan spasi saja")
            return False
        if not nama.replace(" ", ""):
            self.set_validation_status("nama", False, "Nama tidak boleh kosong")
            return False
        self.set_validation_status("nama", True, "Nama valid")
        return True

    def validate_email(self):
        email = self.email_var.get().strip()
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not email:
            self.set_validation_status("email", False, "Email tidak boleh kosong")
            return False
        if not re.fullmatch(pattern, email):
            self.set_validation_status("email", False, "Format email tidak valid")
            return False
        self.set_validation_status("email", True, "Email valid")
        return True

    def validate_phone(self):
        phone = self.phone_var.get().strip()
        if not phone:
            self.set_validation_status("phone", False, "Nomor telepon tidak boleh kosong")
            return False
        if not re.fullmatch(r"08\d{8,11}", phone):
            self.set_validation_status("phone", False, "Gunakan 10–13 digit, diawali 08")
            return False
        self.set_validation_status("phone", True, "Nomor telepon valid")
        return True

    def validate_password(self):
        password = self.password_var.get()
        if len(password) < 8:
            self.set_validation_status("password", False, "Password minimal 8 karakter")
            return False
        if not re.search(r"[a-zA-Z]", password) or not re.search(r"\d", password):
            self.set_validation_status("password", False, "Harus mengandung huruf dan angka")
            return False
        self.set_validation_status("password", True, "Password valid")
        if self.confirm_password_var.get():
            self.validate_confirm_password()
        return True

    def validate_confirm_password(self):
        password = self.password_var.get()
        confirm = self.confirm_password_var.get()
        if not confirm:
            self.set_validation_status(
                "confirm_password", False, "Konfirmasi password tidak boleh kosong"
            )
            return False
        if password != confirm:
            self.set_validation_status("confirm_password", False, "Password tidak sama")
            return False
        self.set_validation_status("confirm_password", True, "Password cocok")
        return True

    def validate_age(self):
        value = self.age_var.get().strip()
        if not value:
            self.set_validation_status("age", False, "Umur tidak boleh kosong")
            return False
        try:
            age = int(value)
        except ValueError:
            self.set_validation_status("age", False, "Umur harus berupa angka")
            return False
        if age < 13:
            self.set_validation_status("age", False, "Umur minimal 13 tahun")
            return False
        if age > 100:
            self.set_validation_status("age", False, "Umur maksimal 100 tahun")
            return False
        self.set_validation_status("age", True, "Umur valid")
        return True

    def validate_agreement(self):
        is_agreed = self.agree_var.get()
        self.validation_status["agree"] = is_agreed
        self.update_submit_button()

    def update_submit_button(self):
        valid_count = sum(bool(status) for status in self.validation_status.values())
        total_fields = len(self.validation_status)
        percentage = valid_count / total_fields * 100

        if hasattr(self, "progress_var"):
            self.progress_var.set(percentage)
            self.progress_label.config(
                text=f"{percentage:.0f}% Complete ({valid_count}/{total_fields} fields)"
            )

        if hasattr(self, "submit_btn") and not self.is_loading:
            if valid_count == total_fields:
                self.submit_btn.config(state=tk.NORMAL, bg="#15803d")
            else:
                self.submit_btn.config(state=tk.DISABLED, bg="#94a3b8")

    def final_validation(self):
        checks = [
            self.validate_nama(),
            self.validate_email(),
            self.validate_phone(),
            self.validate_password(),
            self.validate_confirm_password(),
            self.validate_age(),
        ]
        self.validate_agreement()

        if not all(checks) or not self.agree_var.get():
            errors = [
                label for key, label in [
                    ("nama", "Nama lengkap"),
                    ("email", "Email"),
                    ("phone", "Nomor telepon"),
                    ("password", "Password"),
                    ("confirm_password", "Konfirmasi password"),
                    ("age", "Umur"),
                ] if not self.validation_status[key]
            ]
            if not self.agree_var.get():
                errors.append("Persetujuan syarat dan ketentuan")
            messagebox.showerror(
                "Validasi Gagal",
                "Perbaiki bagian berikut terlebih dahulu:\n\n"
                + "\n".join(f"• {error}" for error in errors),
                parent=self.window,
            )
            return False
        return True

    def submit_form(self):
        if self.is_loading:
            return
        try:
            if not self.final_validation():
                return

            self.is_loading = True
            self.show_loading()
            user_data = {
                "nama": self.nama_var.get().strip(),
                "email": self.email_var.get().strip(),
                "phone": self.phone_var.get().strip(),
                "age": int(self.age_var.get()),
                "gender": self.gender_var.get(),
                "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.window.after(1200, lambda: self.complete_registration(user_data))
        except Exception as exc:
            self.is_loading = False
            self.hide_loading()
            messagebox.showerror("Error", f"Terjadi kesalahan: {exc}", parent=self.window)

    def show_loading(self):
        self.submit_btn.config(text="MEMPROSES...", state=tk.DISABLED, bg="#d97706")
        for name in (
            "nama_entry", "email_entry", "phone_entry",
            "password_entry", "confirm_password_entry", "age_spinbox"
        ):
            widget = getattr(self, name, None)
            if widget:
                widget.config(state=tk.DISABLED)
        self.agree_checkbox.config(state=tk.DISABLED)

    def hide_loading(self):
        self.is_loading = False
        for name in (
            "nama_entry", "email_entry", "phone_entry",
            "password_entry", "confirm_password_entry", "age_spinbox"
        ):
            widget = getattr(self, name, None)
            if widget:
                widget.config(state=tk.NORMAL)
        self.agree_checkbox.config(state=tk.NORMAL)
        self.submit_btn.config(text="DAFTAR SEKARANG")
        self.update_submit_button()

    def complete_registration(self, user_data):
        self.hide_loading()
        message = (
            "REGISTRASI BERHASIL!\n\n"
            f"Nama: {user_data['nama']}\n"
            f"Email: {user_data['email']}\n"
            f"Telepon: {user_data['phone']}\n"
            f"Umur: {user_data['age']} tahun\n"
            f"Jenis Kelamin: {user_data['gender']}\n"
            f"Tanggal Daftar: {user_data['registration_date']}\n\n"
            "Selamat datang di aplikasi kami!"
        )
        messagebox.showinfo("Registrasi Berhasil", message, parent=self.window)

        if messagebox.askyesno(
            "Reset Form", "Ingin mendaftarkan pengguna lain?", parent=self.window
        ):
            self.reset_form()
        else:
            self.window.destroy()

    def reset_form(self):
        self.nama_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.password_var.set("")
        self.confirm_password_var.set("")
        self.age_var.set("18")
        self.gender_var.set("Pria")
        self.agree_var.set(False)

        for key in self.validation_status:
            self.validation_status[key] = False

        for field in ("nama", "email", "phone", "password", "confirm_password", "age"):
            getattr(self, f"{field}_indicator").config(fg="#dc2626")
            hint = getattr(self, f"{field}_hint")
            hint.config(fg="#64748b")

        self.is_loading = False
        self.submit_btn.config(text="DAFTAR SEKARANG")
        self.update_submit_button()

    def jalankan(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = RegistrasiApp()
    app.jalankan()
