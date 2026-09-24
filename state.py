import tkinter as tk
from tkinter import messagebox


class AplikasiBiodata(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Sistem Biodata Mahasiswa")
        self.geometry("520x680")
        self.resizable(True, True)

        # Database pengguna sederhana (username: password)
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456",
        }

        self.current_user = None
        self.frame_aktif = None

        # Siapkan struktur tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Alur awal: kunci akses dan paksa ke halaman login
        self._pindah_ke(self.frame_login)

    # ------------------ SISTEM FRAME & NAVIGASI ------------------
    def _pindah_ke(self, frame_tujuan):
        """Menyembunyikan frame sebelumnya dan menampilkan frame target."""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # Fokus otomatis pada input pertama
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())

    def _buat_menu(self):
        """Menu bar hanya muncul saat user sudah berstatus login."""
        self.menu_bar = tk.Menu(master=self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(master=self.menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        """Menghapus menu bar saat posisi logout / di halaman login."""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    def _update_title(self):
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa — Sesi: {self.current_user}")
        else:
            self.title("Login - Sistem Biodata Mahasiswa")

    # ------------------ HALAMAN 1: LOGIN (GERBANG AWAL) ------------------
    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=30, pady=40)
        self.frame_login.grid_columnconfigure(0, weight=0)
        self.frame_login.grid_columnconfigure(1, weight=1)

        # Judul Form Login
        tk.Label(
            self.frame_login,
            text="LOGIN SISTEM",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 25))

        # Username Input
        tk.Label(self.frame_login, text="Username:", font=("Arial", 11)).grid(
            row=1, column=0, sticky="W", pady=8
        )
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 11))
        self.entry_username.grid(row=1, column=1, pady=8, sticky="EW")

        # Password Input
        tk.Label(self.frame_login, text="Password:", font=("Arial", 11)).grid(
            row=2, column=0, sticky="W", pady=8
        )
        self.entry_password = tk.Entry(
            self.frame_login, font=("Arial", 11), show="*"
        )
        self.entry_password.grid(row=2, column=1, pady=8, sticky="EW")

        # Tombol Aksi Login
        self.btn_login = tk.Button(
            self.frame_login,
            text="Masuk",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            cursor="hand2",
            command=self._coba_login,
        )
        self.btn_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="EW")

        # Shortcut Enter pada login
        self.entry_username.bind(
            "<Return>", lambda e: self.entry_password.focus_set()
        )
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Petunjuk Akun Uji Coba
        info_label = tk.Label(
            self.frame_login,
            text="Akun tersedia:\n• admin (password: 123)\n• user1 (password: password1)\n• mahasiswa (password: 123456)",
            font=("Arial", 9),
            fg="#64748b",
            justify=tk.LEFT,
        )
        info_label.grid(row=4, column=0, columnspan=2, pady=10, sticky="W")

    def _coba_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning(
                "Peringatan", "Username dan Password tidak boleh kosong."
            )
            self.entry_username.focus_set()
            return

        if (
            username in self.users_db
            and self.users_db[username] == password
        ):
            self.current_user = username
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")

            # Pasang menu dan alihkan ke dashboard form biodata
            self._buat_menu()
            self._reset_form_biodata()
            self._update_title()
            self._pindah_ke(self.frame_biodata)

            # Bersihkan field input login
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            messagebox.showerror(
                "Login Gagal", "Username atau password yang dimasukkan salah."
            )
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _logout(self):
        if messagebox.askyesno(
            "Konfirmasi Logout", f"Yakin ingin keluar dari akun {self.current_user}?"
        ):
            self.current_user = None
            self._hapus_menu()
            self._update_title()
            self._reset_form_biodata()
            self._pindah_ke(self.frame_login)
            self.entry_username.focus_set()

    # ------------------ HALAMAN 2: FORM BIODATA (SETELAH LOGIN) ------------------
    def _buat_tampilan_biodata(self):
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=10)

        # Variabel kontrol data
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar(value=0)

        # Tracing untuk validasi tombol submit secara real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        # Header Form
        label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Arial", 15, "bold"),
        )
        label_judul.pack(pady=10)

        # Container Input
        frame_input = tk.Frame(
            master=self.frame_biodata,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=15,
            pady=12,
        )
        frame_input.pack(fill=tk.X, expand=False)
        frame_input.columnconfigure(1, weight=1)

        # Nama
        tk.Label(frame_input, text="Nama Lengkap:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="W", pady=5
        )
        self.entry_nama = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_nama
        )
        self.entry_nama.grid(row=0, column=1, sticky="EW", pady=5)

        # NIM
        tk.Label(frame_input, text="NIM:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="W", pady=5
        )
        self.entry_nim = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_nim
        )
        self.entry_nim.grid(row=1, column=1, sticky="EW", pady=5)

        # Jurusan
        tk.Label(frame_input, text="Jurusan:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="W", pady=5
        )
        self.entry_jurusan = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_jurusan
        )
        self.entry_jurusan.grid(row=2, column=1, sticky="EW", pady=5)

        # Alamat (Text Area + Scrollbar)
        tk.Label(frame_input, text="Alamat:", font=("Arial", 10)).grid(
            row=3, column=0, sticky="NW", pady=5
        )
        frame_alamat = tk.Frame(frame_input, relief=tk.SUNKEN, borderwidth=1)
        frame_alamat.grid(row=3, column=1, sticky="EW", pady=5)

        scrollbar_alamat = tk.Scrollbar(frame_alamat)
        scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_alamat = tk.Text(
            frame_alamat,
            height=4,
            font=("Arial", 10),
            yscrollcommand=scrollbar_alamat.set,
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_alamat.config(command=self.text_alamat.yview)

        # Jenis Kelamin
        tk.Label(frame_input, text="Jenis Kelamin:", font=("Arial", 10)).grid(
            row=4, column=0, sticky="W", pady=5
        )
        frame_jk = tk.Frame(frame_input)
        frame_jk.grid(row=4, column=1, sticky="W", pady=5)

        tk.Radiobutton(
            frame_jk, text="Pria", variable=self.var_jk, value="Pria"
        ).pack(side=tk.LEFT, padx=(0, 15))
        tk.Radiobutton(
            frame_jk, text="Wanita", variable=self.var_jk, value="Wanita"
        ).pack(side=tk.LEFT)

        # Checkbox Persetujuan
        check_setuju = tk.Checkbutton(
            frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 9),
            command=self.validate_form,
        )
        check_setuju.grid(row=5, column=0, columnspan=2, sticky="W", pady=10)

        # Tombol Submit (status awal: DISABLED)
        self.btn_submit = tk.Button(
            self.frame_biodata,
            text="Simpan Data Biodata",
            font=("Arial", 11, "bold"),
            command=self.submit_data,
            state=tk.DISABLED,
        )
        self.btn_submit.pack(fill=tk.X, pady=10)

        # Shortcut Enter pada entry
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)

        # Preview Data Tersimpan
        self.label_hasil = tk.Label(
            self.frame_biodata,
            text="",
            font=("Arial", 10),
            justify=tk.LEFT,
            fg="#1e293b",
        )
        self.label_hasil.pack(anchor="w", padx=5, pady=5)

    # ------------------ LOGIKA VALIDASI & AKSI BIODATA ------------------
    def validate_form(self, *args):
        """Tombol submit hanya aktif jika nama, nim, jurusan, dan persetujuan terisi."""
        nama_ada = self.var_nama.get().strip() != ""
        nim_ada = self.var_nim.get().strip() != ""
        jurusan_ada = self.var_jurusan.get().strip() != ""
        setuju = self.var_setuju.get() == 1

        if nama_ada and nim_ada and jurusan_ada and setuju:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def submit_shortcut(self, event=None):
        if self.btn_submit["state"] == tk.NORMAL:
            self.submit_data()

    def submit_data(self):
        if self.var_setuju.get() == 0:
            messagebox.showwarning(
                "Peringatan", "Anda wajib mencentang persetujuan data."
            )
            return

        nama = self.entry_nama.get().strip()
        nim = self.entry_nim.get().strip()
        jurusan = self.entry_jurusan.get().strip()
        alamat = self.text_alamat.get("1.0", tk.END).strip()
        jenis_kelamin = self.var_jk.get()

        if not alamat:
            messagebox.showwarning("Input Kosong", "Field alamat belum diisi.")
            self.text_alamat.focus_set()
            return

        hasil = (
            f"Nama: {nama}\n"
            f"NIM: {nim}\n"
            f"Jurusan: {jurusan}\n"
            f"Jenis Kelamin: {jenis_kelamin}\n"
            f"Alamat: {alamat}"
        )
        messagebox.showinfo("Berhasil Disimpan", hasil)
        self.label_hasil.config(text=f"DATA TERSIMPAN:\n\n{hasil}")

    def _reset_form_biodata(self):
        """Mengosongkan isian formulir."""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")
        self.btn_submit.config(state=tk.DISABLED)

    def simpan_hasil(self):
        """Menulis preview data ke berkas txt."""
        teks = self.label_hasil.cget("text")
        if not teks or "DATA TERSIMPAN" not in teks:
            messagebox.showwarning(
                "Peringatan", "Belum ada data tersimpan yang dapat diekspor."
            )
            return

        with open("biodata_tersimpan.txt", "w", encoding="utf-8") as file:
            file.write(teks)
        messagebox.showinfo(
            "Berhasil", "Data berhasil diekspor ke berkas 'biodata_tersimpan.txt'."
        )

    def keluar_aplikasi(self):
        if messagebox.askokcancel("Keluar", "Yakin ingin menutup aplikasi?"):
            self.destroy()


if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()