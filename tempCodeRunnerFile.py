import tkinter as tk
from tkinter import messagebox
import datetime

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

        # ------------------ CUSTOM MESSAGE BOX ------------------
    def custom_messagebox(self, title, message, tipe="info", confirm=False):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.geometry("390x230")
        popup.resizable(False, False)
        popup.configure(bg="#f8fafc")

        # Supaya popup berada di tengah window utama
        popup.transient(self)
        popup.grab_set()

        # Warna berdasarkan tipe popup
        warna = {
            "success": "#16a34a",
            "info": "#2563eb",
            "warning": "#f59e0b",
            "error": "#dc2626"
        }

        icon = {
            "success": "✓",
            "info": "i",
            "warning": "!",
            "error": "×"
        }

        warna_utama = warna.get(tipe, "#2563eb")
        icon_popup = icon.get(tipe, "i")

        # Header
        header = tk.Frame(
            popup,
            bg=warna_utama,
            height=65
        )
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Icon
        label_icon = tk.Label(
            header,
            text=icon_popup,
            font=("Segoe UI", 22, "bold"),
            bg=warna_utama,
            fg="white"
        )
        label_icon.pack(side=tk.LEFT, padx=(25, 10))

        # Judul
        label_title = tk.Label(
            header,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg=warna_utama,
            fg="white"
        )
        label_title.pack(side=tk.LEFT)

        # Isi pesan
        label_message = tk.Label(
            popup,
            text=message,
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg="#334155",
            justify=tk.CENTER,
            wraplength=330
        )
        label_message.pack(
            fill=tk.X,
            padx=25,
            pady=(25, 15)
        )

        # Container tombol
        frame_button = tk.Frame(
            popup,
            bg="#f8fafc"
        )
        frame_button.pack(fill=tk.X, pady=(5, 20))

        # Tombol OK
        def tutup_popup():
            popup.grab_release()
            popup.destroy()

        btn_ok = tk.Button(
            frame_button,
            text="OK",
            font=("Segoe UI", 10, "bold"),
            bg=warna_utama,
            fg="white",
            activebackground=warna_utama,
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=25,
            pady=8,
            cursor="hand2",
            command=tutup_popup
        )
        btn_ok.pack(side=tk.RIGHT, padx=(5, 25))

        # Kalau popup konfirmasi
        if confirm:
            def batal():
                popup.grab_release()
                popup.destroy()

            btn_ok.config(text="Ya")

            btn_batal = tk.Button(
                frame_button,
                text="Batal",
                font=("Segoe UI", 10),
                bg="#e2e8f0",
                fg="#334155",
                activebackground="#cbd5e1",
                relief=tk.FLAT,
                bd=0,
                padx=20,
                pady=8,
                cursor="hand2",
                command=batal
            )
            btn_batal.pack(side=tk.RIGHT)

        # Enter = OK
        popup.bind("<Return>", lambda event: tutup_popup())
        popup.bind("<Escape>", lambda event: tutup_popup())

        # Fokus
        popup.focus_force()

        # Posisi tengah layar
        popup.update_idletasks()

        x = self.winfo_x() + (self.winfo_width() // 2) - (390 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (230 // 2)

        popup.geometry(f"390x230+{x}+{y}")
    # ------------------ HALAMAN 1: LOGIN (GERBANG AWAL) ------------------
    def button_hover(self, button, normal, hover):
            button.bind(
                "<Enter>",
                lambda e: button.config(bg=hover)
            )
    
            button.bind(
                "<Leave>",
                lambda e: button.config(bg=normal)
            )
    
    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(
            master=self,
            padx=45,
            pady=40,
            bg="#f1f5f9"
        )

        self.frame_login.grid_columnconfigure(0, weight=1)

        # =========================
        # JUDUL
        # =========================
        tk.Label(
            self.frame_login,
            text="LOGIN SISTEM",
            font=("Segoe UI", 20, "bold"),
            bg="#f1f5f9",
            fg="#0f172a"
        ).grid(
            row=0,
            column=0,
            pady=(20, 25)
        )

        # =========================
        # CARD LOGIN
        # =========================
        card_login = tk.Frame(
            self.frame_login,
            bg="#ffffff",
            padx=30,
            pady=30,
            highlightbackground="#e2e8f0",
            highlightthickness=1
        )

        card_login.grid(
            row=1,
            column=0,
            sticky="EW"
        )

        card_login.columnconfigure(0, weight=1)

        # =========================
        # USERNAME
        # =========================
        tk.Label(
            card_login,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).grid(
            row=0,
            column=0,
            sticky="W",
            pady=(0, 6)
        )

        self.entry_username = tk.Entry(
            card_login,
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            bg="#f8fafc",
            fg="#0f172a",
            insertbackground="#2563eb"
        )

        self.entry_username.grid(
            row=1,
            column=0,
            sticky="EW",
            ipady=8,
            pady=(0, 18)
        )

        # =========================
        # PASSWORD
        # =========================
        tk.Label(
            card_login,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).grid(
            row=2,
            column=0,
            sticky="W",
            pady=(0, 6)
        )

        self.entry_password = tk.Entry(
            card_login,
            font=("Segoe UI", 11),
            show="*",
            relief=tk.FLAT,
            bg="#f8fafc",
            fg="#0f172a",
            insertbackground="#2563eb"
        )

        self.entry_password.grid(
            row=3,
            column=0,
            sticky="EW",
            ipady=8,
            pady=(0, 20)
        )

        # =========================
        # BUTTON LOGIN
        # =========================
        self.btn_login = tk.Button(
            card_login,
            text="Masuk",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=15,
            pady=10,
            command=self._coba_login
        )

        self.btn_login.grid(
            row=4,
            column=0,
            sticky="EW"
        )

        self.button_hover(
            self.btn_login,
            "#2563eb",
            "#1d4ed8"
        )

        # =========================
        # INFO AKUN
        # =========================
        info_label = tk.Label(
            self.frame_login,
            text=(
                "Akun tersedia:\n"
                "• admin  (password: 123)\n"
                "• user1  (password: password1)\n"
                "• mahasiswa  (password: 123456)"
            ),
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#64748b",
            justify=tk.LEFT
        )

        info_label.grid(
            row=2,
            column=0,
            pady=(15, 10),
            sticky="W"
        )

        # =========================
        # SHORTCUT ENTER
        # =========================
        self.entry_username.bind(
            "<Return>",
            lambda e: self.entry_password.focus_set()
        )

        self.entry_password.bind(
            "<Return>",
            lambda e: self._coba_login()
        )
        
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
                self.custom_messagebox(
                    "Peringatan",
                    "Username dan Password tidak boleh kosong.",
                    "warning"
                )
                self.entry_username.focus_set()
                return

            if (
                username in self.users_db
                and self.users_db[username] == password
            ):
                self.current_user = username
                self.custom_messagebox(
                    "Login Berhasil",
                    f"Selamat datang, {username}!",
                    "success"
                )

                # Pasang menu dan alihkan ke dashboard form biodata
                self._buat_menu()
                self._reset_form_biodata()
                self._update_title()
                self._pindah_ke(self.frame_biodata)

                # Bersihkan field input login
                self.entry_username.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
            else:
                self.custom_messagebox(
                    "Login Gagal",
                    "Username atau password yang dimasukkan salah.",
                    "error"
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
        # =========================
        # FRAME UTAMA
        # =========================
        self.frame_biodata = tk.Frame(
            master=self,
            padx=35,
            pady=25,
            bg="#f1f5f9"
        )

        self.frame_biodata.columnconfigure(0, weight=1)

        # =========================
        # VARIABEL KONTROL DATA
        # =========================
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar(value=0)

        # Validasi tombol submit secara real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        # =========================
        # HEADER
        # =========================
        label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Segoe UI", 20, "bold"),
            bg="#f1f5f9",
            fg="#0f172a"
        )

        label_judul.pack(
            pady=(5, 3)
        )

        label_subjudul = tk.Label(
            master=self.frame_biodata,
            text="Lengkapi informasi data mahasiswa",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg="#64748b"
        )

        label_subjudul.pack(
            pady=(0, 20)
        )

        # =========================
        # CARD INPUT
        # =========================
        frame_input = tk.Frame(
            master=self.frame_biodata,
            bg="#ffffff",
            padx=25,
            pady=25,
            highlightbackground="#e2e8f0",
            highlightthickness=1
        )

        frame_input.pack(
            fill=tk.X,
            expand=False
        )

        frame_input.columnconfigure(
            1,
            weight=1
        )

        # =========================
        # NAMA LENGKAP
        # =========================
        tk.Label(
            frame_input,
            text="Nama Lengkap:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).grid(
            row=0,
            column=0,
            sticky="W",
            pady=7
        )

        self.entry_nama = tk.Entry(
            frame_input,
            font=("Segoe UI", 10),
            textvariable=self.var_nama,
            relief=tk.FLAT,
            bg="#f8fafc",
            fg="#0f172a",
            insertbackground="#2563eb"
        )

        self.entry_nama.grid(
            row=0,
            column=1,
            sticky="EW",
            pady=7,
            padx=(15, 0),
            ipady=7
        )

        # =========================
        # NIM
        # =========================
        tk.Label(
            frame_input,
            text="NIM:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).grid(
            row=1,
            column=0,
            sticky="W",
            pady=7
        )

        self.entry_nim = tk.Entry(
            frame_input,
            font=("Segoe UI", 10),
            textvariable=self.var_nim,
            relief=tk.FLAT,
            bg="#f8fafc",
            fg="#0f172a",
            insertbackground="#2563eb"
        )

        self.entry_nim.grid(
            row=1,
            column=1,
            sticky="EW",
            pady=7,
            padx=(15, 0),
            ipady=7
        )

        # =========================
        # JURUSAN
        # =========================
        tk.Label(
            frame_input,
            text="Jurusan:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).grid(
            row=2,
            column=0,
            sticky="W",
            pady=7
        )

        self.entry_jurusan = tk.Entry(
            frame_input,
            font=("Segoe UI", 10),
            textvariable=self.var_jurusan,
            relief=tk.FLAT,
            bg="#f8fafc",
            fg="#0f172a",
            insertbackground="#2563eb"
        )

        self.entry_jurusan.grid(
            row=2,
            column=1,
            sticky="EW",
            pady=7,
            padx=(15, 0),
            ipady=7
        )

        # =========================
        # ALAMAT
        # =========================
        tk.Label(
            frame_input,
            text="Alamat:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).grid(
            row=3,
            column=0,
            sticky="NW",
            pady=7
        )

        # Container textarea
        frame_alamat = tk.Frame(
            frame_input,
            bg="#f8fafc",
            highlightbackground="#e2e8f0",
            highlightthickness=1
        )

        frame_alamat.grid(
            row=3,
            column=1,
            sticky="EW",
            pady=7,
            padx=(15, 0)
        )

        # Scrollbar alamat
        scrollbar_alamat = tk.Scrollbar(
            frame_alamat
        )

        scrollbar_alamat.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        # Text area
        self.text_alamat = tk.Text(
            frame_alamat,
            height=4,
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg="#0f172a",
            insertbackground="#2563eb",
            relief=tk.FLAT,
            yscrollcommand=scrollbar_alamat.set
        )

        self.text_alamat.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=8,
            pady=8
        )

        scrollbar_alamat.config(
            command=self.text_alamat.yview
        )

        # =========================
        # JENIS KELAMIN
        # =========================
        tk.Label(
            frame_input,
            text="Jenis Kelamin:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#334155"
        ).grid(
            row=4,
            column=0,
            sticky="W",
            pady=7
        )

        frame_jk = tk.Frame(
            frame_input,
            bg="#ffffff"
        )

        frame_jk.grid(
            row=4,
            column=1,
            sticky="W",
            pady=7,
            padx=(15, 0)
        )

        # Pria
        tk.Radiobutton(
            frame_jk,
            text="Pria",
            variable=self.var_jk,
            value="Pria",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#334155",
            activebackground="#ffffff",
            activeforeground="#334155",
            selectcolor="#f8fafc"
        ).pack(
            side=tk.LEFT,
            padx=(0, 20)
        )

        # Wanita
        tk.Radiobutton(
            frame_jk,
            text="Wanita",
            variable=self.var_jk,
            value="Wanita",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#334155",
            activebackground="#ffffff",
            activeforeground="#334155",
            selectcolor="#f8fafc"
        ).pack(
            side=tk.LEFT
        )

        # =========================
        # CHECKBOX PERSETUJUAN
        # =========================
        check_setuju = tk.Checkbutton(
            frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#334155",
            activebackground="#ffffff",
            activeforeground="#334155",
            selectcolor="#f8fafc",
            command=self.validate_form
        )

        check_setuju.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="W",
            pady=(15, 0)
        )

        # =========================
        # TOMBOL SUBMIT
        # =========================
        self.btn_submit = tk.Button(
            self.frame_biodata,
            text="Simpan Data Biodata",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            disabledforeground="#94a3b8",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=15,
            pady=10,
            command=self.submit_data,
            state=tk.DISABLED
        )

        self.btn_submit.pack(
            fill=tk.X,
            pady=(20, 10)
        )

        self.button_hover(
            self.btn_submit,
            "#2563eb",
            "#1d4ed8"
        )

        # =========================
        # SHORTCUT ENTER
        # =========================
        self.entry_nama.bind(
            "<Return>",
            self.submit_shortcut
        )

        self.entry_nim.bind(
            "<Return>",
            self.submit_shortcut
        )

        self.entry_jurusan.bind(
            "<Return>",
            self.submit_shortcut
        )

        # =========================
        # PREVIEW DATA TERSIMPAN
        # =========================
        self.label_hasil = tk.Label(
            self.frame_biodata,
            text="",
            font=("Segoe UI", 10),
            justify=tk.LEFT,
            bg="#f1f5f9",
            fg="#1e293b"
        )

        self.label_hasil.pack(
            anchor="w",
            padx=5,
            pady=5
        )
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
            """Submit data biodata dengan validasi lengkap"""
            try:
                # Cek checkbox
                if self.var_setuju.get() == 0:
                    messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                    return

                # Ambil data dari form
                nama = self.entry_nama.get().strip()
                nim = self.entry_nim.get().strip()
                jurusan = self.entry_jurusan.get().strip()
                alamat = self.text_alamat.get("1.0", tk.END).strip()
                jenis_kelamin = self.var_jk.get()

                # Validasi field kosong
                if not nama or not nim or not jurusan:
                    messagebox.showwarning("Input Kosong", "Nama, NIM, dan Jurusan harus diisi!")
                    return

                    # Validasi format NIM (harus angka dan minimal 8 digit)
                if not nim.isdigit() or len(nim) < 8:
                    messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
                    self.entry_nim.focus_set()
                    return

                # Validasi nama (tidak boleh hanya angka)
                if nama.isdigit():
                    messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                    self.entry_nama.focus_set()
                    return

                # Tampilkan hasil
                hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
                self.custom_messagebox(
                    "Data Tersimpan",
                    hasil,
                    "success"
                )

                # Tampilkan hasil di label dengan info user
                hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
                self.label_hasil.config(text=hasil_lengkap)

            except Exception as e:
                self.custom_messagebox(
                    "Error",
                    f"Terjadi kesalahan saat memproses data:\n{str(e)}",
                    "error"
                )

    def simpan_hasil(self):
            """Simpan hasil biodata ke file dengan error handling"""
            try:
                hasil_tersimpan = self.label_hasil.cget("text")

                if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                    messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
                    return

                # Buat nama file dengan timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"biodata_{self.current_user}_{timestamp}.txt"

                with open(filename, "w", encoding="utf-8") as file:
                    file.write(f"Data disimpan oleh: {self.current_user}\n")
                    file.write(f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write("-" * 50 + "\n")
                    file.write(hasil_tersimpan)

                messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")

            except PermissionError:
                messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")


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


    def keluar_aplikasi(self):
            if messagebox.askokcancel("Keluar", "Yakin ingin menutup aplikasi?"):
                self.destroy()


if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()