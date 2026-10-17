import tkinter as tk
from tkinter import ttk, messagebox


class QuizInteraktif:
    DURASI_SOAL = 15

    FILE_SOAL = "soal_quiz.json"

    @classmethod
    def muat_soal(cls):
        """Memuat daftar soal dari file JSON di folder yang sama."""
        import json
        from pathlib import Path

        file_soal = Path(__file__).resolve().parent / cls.FILE_SOAL
        try:
            with file_soal.open("r", encoding="utf-8") as file:
                soal = json.load(file)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"File soal tidak ditemukan: {file_soal}. "
                "Pastikan soal_quiz.json berada di folder yang sama."
            ) from exc
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Format JSON pada {file_soal.name} tidak valid: {exc}"
            ) from exc

        if not isinstance(soal, list) or not soal:
            raise ValueError("File soal harus berisi list soal dan tidak boleh kosong.")

        for nomor, item in enumerate(soal, start=1):
            if not all(k in item for k in ("pertanyaan", "pilihan", "jawaban", "penjelasan")):
                raise ValueError(f"Soal nomor {nomor} memiliki field yang belum lengkap.")
            if len(item["pilihan"]) != 4:
                raise ValueError(f"Soal nomor {nomor} harus memiliki tepat 4 pilihan.")
            if not isinstance(item["jawaban"], int) or not 0 <= item["jawaban"] < 4:
                raise ValueError(f"Indeks jawaban soal nomor {nomor} harus 0 sampai 3.")

        return soal

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Interaktif | Python")
        self.root.geometry("860x650")
        self.root.minsize(760, 600)
        self.root.configure(bg="#F3F6FC")

        # Muat soal dari file JSON sebelum membuat state kuis.
        try:
            self.SOAL = self.muat_soal()
        except (FileNotFoundError, ValueError) as error:
            messagebox.showerror("Kesalahan File Soal", str(error))
            self.root.destroy()
            raise

        self.indeks_soal = 0
        self.skor = 0
        self.jawaban_pengguna = [None] * len(self.SOAL)
        self.status_soal = ["belum"] * len(self.SOAL)
        # Setiap soal punya timer sendiri; waktu tidak di-reset saat navigasi.
        self.waktu_per_soal = [self.DURASI_SOAL] * len(self.SOAL)
        self.sisa_waktu = self.DURASI_SOAL
        self.timer_job = None
        self.feedback_job = None
        self.sedang_feedback = False
        self.sudah_selesai = False

        self.jawaban_var = tk.IntVar(value=-1)  # -1 berarti belum ada pilihan
        self.status_var = tk.StringVar(value="Pilih jawaban, lalu tekan Enter.")
        self.timer_var = tk.StringVar(value="")
        self.skor_var = tk.StringVar(value="Skor: 0")
        self.nomor_var = tk.StringVar(value="Soal 1 dari 10")

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(
            "Quiz.Horizontal.TProgressbar",
            troughcolor="#E3E9F4",
            background="#4263EB",
            bordercolor="#E3E9F4",
            lightcolor="#4263EB",
            darkcolor="#4263EB",
            thickness=12,
        )

        self.buat_interface()
        self.root.bind("<Return>", self.submit_jawaban)
        self.root.bind("<Escape>", self.skip_soal)
        self.root.protocol("WM_DELETE_WINDOW", self.konfirmasi_keluar)

        self.tampilkan_soal()
        self.jalankan_timer()

    def buat_interface(self):
        header = tk.Frame(self.root, bg="#172554", padx=24, pady=18)
        header.pack(fill=tk.X)

        tk.Label(
            header, text="QUIZ INTERAKTIF",
            font=("Segoe UI", 20, "bold"),
            fg="white", bg="#172554"
        ).pack(anchor="w")

        tk.Label(
            header, text="Uji pemahaman Python dan Tkinter",
            font=("Segoe UI", 10),
            fg="#C7D2FE", bg="#172554"
        ).pack(anchor="w", pady=(3, 0))

        main = tk.Frame(self.root, bg="#F3F6FC", padx=28, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        top_row = tk.Frame(main, bg="#F3F6FC")
        top_row.pack(fill=tk.X)

        tk.Label(
            top_row, textvariable=self.nomor_var,
            font=("Segoe UI", 11, "bold"),
            fg="#334155", bg="#F3F6FC"
        ).pack(side=tk.LEFT)

        tk.Label(
            top_row, textvariable=self.skor_var,
            font=("Segoe UI", 11, "bold"),
            fg="#2563EB", bg="#F3F6FC"
        ).pack(side=tk.RIGHT)

        self.progress = ttk.Progressbar(
            main, style="Quiz.Horizontal.TProgressbar",
            orient="horizontal", mode="determinate",
            maximum=len(self.SOAL), value=0
        )
        self.progress.pack(fill=tk.X, pady=(10, 10))

        # Navigasi nomor soal: bisa kembali ke soal mana pun.
        nav_wrap = tk.Frame(main, bg="#F3F6FC")
        nav_wrap.pack(fill=tk.X, pady=(0, 14))

        tk.Label(
            nav_wrap,
            text="Navigasi soal:",
            font=("Segoe UI", 9, "bold"),
            fg="#475569",
            bg="#F3F6FC",
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.nav_frame = tk.Frame(nav_wrap, bg="#F3F6FC")
        self.nav_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.nav_buttons = []
        for nomor in range(len(self.SOAL)):
            tombol = tk.Button(
                self.nav_frame,
                text=str(nomor + 1),
                width=3,
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                padx=3,
                pady=5,
                cursor="hand2",
                command=lambda idx=nomor: self.pindah_ke_soal(idx),
            )
            tombol.pack(side=tk.LEFT, padx=2, pady=2)
            self.nav_buttons.append(tombol)

        self.card = tk.Frame(
            main, bg="white", padx=24, pady=22,
            highlightthickness=1, highlightbackground="#DCE4F0"
        )
        self.card.pack(fill=tk.BOTH, expand=True)

        self.timer_label = tk.Label(
            self.card, textvariable=self.timer_var,
            font=("Segoe UI", 11, "bold"),
            fg="#B45309", bg="white"
        )
        self.timer_label.pack(anchor="e")

        self.pertanyaan_label = tk.Label(
            self.card, text="", font=("Segoe UI", 15, "bold"),
            fg="#172554", bg="white", wraplength=690,
            justify="left", anchor="w"
        )
        self.pertanyaan_label.pack(fill=tk.X, anchor="w", pady=(12, 18))

        self.opsi_frame = tk.Frame(self.card, bg="white")
        self.opsi_frame.pack(fill=tk.X)

        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(
                self.opsi_frame, text="", variable=self.jawaban_var,
                value=i, font=("Segoe UI", 11),
                fg="#334155", bg="white", activebackground="white",
                selectcolor="#DBEAFE", anchor="w", justify="left",
                wraplength=650, padx=12, pady=9, cursor="hand2",
                command=self.pilihan_berubah
            )
            rb.pack(fill=tk.X, pady=3)
            self.radio_buttons.append(rb)

        self.feedback_label = tk.Label(
            self.card, textvariable=self.status_var,
            font=("Segoe UI", 10, "bold"), fg="#64748B",
            bg="white", anchor="w", justify="left", wraplength=680
        )
        self.feedback_label.pack(fill=tk.X, pady=(18, 0))

        footer = tk.Frame(main, bg="#F3F6FC")
        footer.pack(fill=tk.X, pady=(16, 0))

        self.skip_button = tk.Button(
            footer, text="Lewati  (Esc)", command=self.skip_soal,
            font=("Segoe UI", 10, "bold"), bg="#E2E8F0",
            fg="#334155", activebackground="#CBD5E1",
            relief=tk.FLAT, padx=18, pady=11, cursor="hand2"
        )
        self.skip_button.pack(side=tk.LEFT)

        self.submit_button = tk.Button(
            footer, text="Kunci Jawaban  (Enter)",
            command=self.submit_jawaban,
            font=("Segoe UI", 10, "bold"), bg="#4263EB",
            fg="white", activebackground="#3451C6",
            activeforeground="white", relief=tk.FLAT,
            padx=20, pady=11, cursor="hand2"
        )
        self.submit_button.pack(side=tk.RIGHT)

        tk.Label(
            self.root, text="Enter: submit jawaban    •    Esc: lewati soal",
            font=("Segoe UI", 9), fg="#64748B",
            bg="#F3F6FC", pady=8
        ).pack(fill=tk.X)

    def tampilkan_soal(self):
        if self.indeks_soal >= len(self.SOAL):
            self.tampilkan_hasil()
            return

        soal = self.SOAL[self.indeks_soal]
        jawaban_tersimpan = self.jawaban_pengguna[self.indeks_soal]
        self.jawaban_var.set(-1 if jawaban_tersimpan is None else jawaban_tersimpan)
        self.sisa_waktu = self.waktu_per_soal[self.indeks_soal]
        self.sedang_feedback = False

        self.nomor_var.set(f"Soal {self.indeks_soal + 1} dari {len(self.SOAL)}")
        self.skor_var.set(f"Skor: {self.skor}")
        self.progress.configure(
            value=sum(status != "belum" for status in self.status_soal)
        )
        self.pertanyaan_label.config(text=soal["pertanyaan"])

        status_saat_ini = self.status_soal[self.indeks_soal]
        sudah_dijawab = status_saat_ini in ("benar", "salah")
        waktu_habis = self.sisa_waktu <= 0

        for i, rb in enumerate(self.radio_buttons):
            rb.config(
                text=f"{chr(65 + i)}. {soal['pilihan'][i]}",
                state=tk.DISABLED if sudah_dijawab or waktu_habis else tk.NORMAL,
                fg="#334155", bg="white",
                selectcolor="#DBEAFE"
            )

        if sudah_dijawab:
            hasil = "Benar" if status_saat_ini == "benar" else "Salah"
            self.status_var.set(
                f"Soal sudah dikunci: jawaban {hasil.lower()}. Jawaban tidak bisa diubah."
            )
            self.feedback_label.config(
                fg="#15803D" if status_saat_ini == "benar" else "#B91C1C",
                bg="white"
            )
            self.submit_button.config(state=tk.DISABLED, text="Jawaban Terkunci")
            self.skip_button.config(state=tk.DISABLED)
            self.batalkan_timer()
        elif waktu_habis:
            self.status_var.set("Waktu soal ini sudah habis. Jawaban tidak bisa diisi lagi.")
            self.feedback_label.config(fg="#B91C1C", bg="white")
            self.submit_button.config(state=tk.DISABLED, text="Waktu Habis")
            self.skip_button.config(state=tk.DISABLED)
            self.batalkan_timer()
        else:
            self.status_var.set("Pilih jawaban. Enter untuk submit, Esc untuk skip.")
            self.feedback_label.config(fg="#64748B", bg="white")
            self.submit_button.config(state=tk.NORMAL, text="Kunci Jawaban  (Enter)")
            self.skip_button.config(state=tk.NORMAL)
        self.update_timer_label()

    def perbarui_navigasi(self):
        """Warna tombol nomor mencerminkan status setiap soal."""
        for idx, tombol in enumerate(self.nav_buttons):
            status = self.status_soal[idx]
            if idx == self.indeks_soal:
                bg, fg = "#4263EB", "white"  # soal yang sedang dibuka
            elif status == "benar":
                bg, fg = "#DCFCE7", "#166534"
            elif status == "salah":
                bg, fg = "#FEE2E2", "#991B1B"
            elif status in ("dilewati", "waktu habis"):
                bg, fg = "#FEF3C7", "#92400E"
            else:
                bg, fg = "#E2E8F0", "#334155"  # belum dijawab

            tombol.config(
                bg=bg, fg=fg, activebackground=bg,
                activeforeground=fg
            )

    def pindah_ke_soal(self, indeks):
        """Pindah ke nomor soal yang dipilih tanpa menghapus jawaban tersimpan."""
        if self.sudah_selesai:
            return

        # Abaikan klik navigasi ketika feedback sedang ditampilkan.
        if self.sedang_feedback:
            return

        if indeks == self.indeks_soal:
            return

        self.batalkan_timer()
        self.batalkan_feedback()
        self.indeks_soal = indeks
        self.tampilkan_soal()
        self.jalankan_timer()

    def pilihan_berubah(self):
        if not self.sedang_feedback and not self.sudah_selesai:
            self.status_var.set("Jawaban dipilih. Tekan Enter atau klik Kunci Jawaban.")
            self.feedback_label.config(fg="#2563EB")

    def submit_jawaban(self, event=None):
        if self.sudah_selesai or self.sedang_feedback:
            return "break"

        pilihan = self.jawaban_var.get()
        if pilihan == -1:
            self.status_var.set("Pilih salah satu jawaban terlebih dahulu.")
            self.feedback_label.config(fg="#DC2626")
            self.animasi_feedback("#FEE2E2")
            return "break"

        self.batalkan_timer()
        self.waktu_per_soal[self.indeks_soal] = self.sisa_waktu
        soal = self.SOAL[self.indeks_soal]
        indeks_pilihan = pilihan
        benar = indeks_pilihan == soal["jawaban"]

        self.jawaban_pengguna[self.indeks_soal] = indeks_pilihan
        self.status_soal[self.indeks_soal] = "benar" if benar else "salah"

        if benar:
            self.status_var.set("Benar! " + soal["penjelasan"])
            self.feedback_label.config(fg="#15803D")
            self.animasi_feedback("#DCFCE7")
        else:
            huruf_benar = chr(65 + soal["jawaban"])
            teks_benar = soal["pilihan"][soal["jawaban"]]
            self.status_var.set(
                f"Belum tepat. Jawaban: {huruf_benar}. {teks_benar}. "
                + soal["penjelasan"]
            )
            self.feedback_label.config(fg="#B91C1C")
            self.animasi_feedback("#FEE2E2")

        self.perbarui_status()
        self.kunci_kontrol()
        self.feedback_job = self.root.after(1500, self.soal_berikutnya)
        return "break"

    def skip_soal(self, event=None):
        if self.sudah_selesai or self.sedang_feedback:
            return "break"

        self.batalkan_timer()
        self.waktu_per_soal[self.indeks_soal] = self.sisa_waktu
        self.jawaban_pengguna[self.indeks_soal] = None
        self.status_soal[self.indeks_soal] = "dilewati"
        self.status_var.set("Soal dilewati. Skor tidak bertambah.")
        self.feedback_label.config(fg="#B45309")
        self.animasi_feedback("#FEF3C7")
        self.perbarui_status()
        self.kunci_kontrol()
        self.feedback_job = self.root.after(700, self.soal_berikutnya)
        return "break"

    def waktu_habis(self):
        self.timer_job = None
        if self.sudah_selesai or self.sedang_feedback:
            return

        indeks = self.indeks_soal
        self.waktu_per_soal[indeks] = 0
        pilihan = self.jawaban_var.get()
        soal = self.SOAL[indeks]

        # Jika pengguna sudah memilih opsi sebelum waktu habis,
        # nilai pilihan itu otomatis meskipun belum menekan Enter.
        if pilihan != -1:
            benar = pilihan == soal["jawaban"]
            self.jawaban_pengguna[indeks] = pilihan
            self.status_soal[indeks] = "benar" if benar else "salah"

            if benar:
                self.status_var.set("Waktu habis, tetapi jawaban yang dipilih benar! " + soal["penjelasan"])
                self.feedback_label.config(fg="#15803D")
                self.animasi_feedback("#DCFCE7")
            else:
                huruf_benar = chr(65 + soal["jawaban"])
                teks_benar = soal["pilihan"][soal["jawaban"]]
                self.status_var.set(
                    f"Waktu habis. Jawaban salah. Jawaban benar: {huruf_benar}. {teks_benar}. "
                    + soal["penjelasan"]
                )
                self.feedback_label.config(fg="#B91C1C")
                self.animasi_feedback("#FEE2E2")
        else:
            self.jawaban_pengguna[indeks] = None
            self.status_soal[indeks] = "waktu habis"
            self.status_var.set("Waktu habis! Tidak ada jawaban yang dipilih, jadi soal ini kosong.")
            self.feedback_label.config(fg="#B91C1C")
            self.animasi_feedback("#FEE2E2")

        self.perbarui_status()
        self.kunci_kontrol()
        self.feedback_job = self.root.after(1200, self.soal_berikutnya)

    def jalankan_timer(self):
        if self.sudah_selesai or self.sedang_feedback:
            return

        status = self.status_soal[self.indeks_soal]
        if status in ("benar", "salah"):
            self.batalkan_timer()
            return

        # Penting: proses waktu habis sebelum keluar dari fungsi.
        # Sebelumnya timer berhenti di 0 tanpa memanggil waktu_habis().
        if self.sisa_waktu <= 0:
            self.sisa_waktu = 0
            self.waktu_per_soal[self.indeks_soal] = 0
            self.update_timer_label()
            self.waktu_habis()
            return

        self.update_timer_label()
        self.sisa_waktu -= 1
        self.waktu_per_soal[self.indeks_soal] = self.sisa_waktu
        self.timer_job = self.root.after(1000, self.jalankan_timer)

    def update_timer_label(self):
        self.timer_var.set(f"Waktu tersisa: {self.sisa_waktu} detik")
        self.timer_label.config(
            fg="#DC2626" if self.sisa_waktu <= 5 else "#B45309"
        )

    def batalkan_timer(self):
        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except tk.TclError:
                pass
            self.timer_job = None

    def batalkan_feedback(self):
        if self.feedback_job is not None:
            try:
                self.root.after_cancel(self.feedback_job)
            except tk.TclError:
                pass
            self.feedback_job = None

    def animasi_feedback(self, warna):
        """Efek visual sederhana dengan mengubah warna kartu."""
        self.card.config(bg=warna)
        for widget in self.card.winfo_children():
            try:
                widget.config(bg=warna)
            except tk.TclError:
                pass
        self.opsi_frame.config(bg=warna)
        for rb in self.radio_buttons:
            rb.config(bg=warna, activebackground=warna)
        self.root.after(250, self.pulihkan_warna)

    def pulihkan_warna(self):
        if not self.winfo_ada():
            return
        self.card.config(bg="white")
        for widget in self.card.winfo_children():
            try:
                widget.config(bg="white")
            except tk.TclError:
                pass
        self.opsi_frame.config(bg="white")
        for rb in self.radio_buttons:
            rb.config(bg="white", activebackground="white")

    def winfo_ada(self):
        try:
            return bool(self.root.winfo_exists())
        except tk.TclError:
            return False

    def kunci_kontrol(self):
        self.sedang_feedback = True
        for rb in self.radio_buttons:
            rb.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)

    def perbarui_status(self):
        # Skor dihitung dari status terkini setiap soal agar tidak dobel
        # ketika pengguna kembali dan mengubah jawaban sebelumnya.
        self.skor = sum(status == "benar" for status in self.status_soal) * 10
        self.skor_var.set(f"Skor: {self.skor}")
        selesai = sum(status != "belum" for status in self.status_soal)
        self.progress.configure(value=selesai)
        self.perbarui_navigasi()

    def soal_berikutnya(self):
        self.feedback_job = None
        self.indeks_soal += 1
        if self.indeks_soal >= len(self.SOAL):
            self.tampilkan_hasil()
            return
        self.tampilkan_soal()
        self.jalankan_timer()

    def tampilkan_hasil(self):
        self.batalkan_timer()
        self.batalkan_feedback()
        self.sudah_selesai = True
        self.sedang_feedback = True

        for widget in self.root.winfo_children():
            widget.destroy()

        total = len(self.SOAL)
        benar = sum(status == "benar" for status in self.status_soal)
        salah = sum(status == "salah" for status in self.status_soal)
        dilewati = sum(
            status in ("dilewati", "waktu habis") for status in self.status_soal
        )
        persentase = round(benar / total * 100)

        container = tk.Frame(self.root, bg="#F3F6FC", padx=30, pady=30)
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            container, text="KUIS SELESAI!",
            font=("Segoe UI", 24, "bold"),
            fg="#172554", bg="#F3F6FC"
        ).pack(pady=(25, 8))

        tk.Label(
            container, text=f"{self.skor} / {total * 10}",
            font=("Segoe UI", 32, "bold"),
            fg="#4263EB", bg="#F3F6FC"
        ).pack()

        tk.Label(
            container, text=f"Nilai: {persentase}%",
            font=("Segoe UI", 16, "bold"),
            fg="#334155", bg="#F3F6FC"
        ).pack(pady=(0, 20))

        ringkasan = (
            f"Jawaban benar : {benar}\n"
            f"Jawaban salah : {salah}\n"
            f"Dilewati / waktu habis : {dilewati}\n"
            f"Total soal : {total}"
        )
        tk.Label(
            container, text=ringkasan, font=("Segoe UI", 12),
            fg="#334155", bg="white", justify="left",
            padx=35, pady=22, relief=tk.FLAT
        ).pack()

        tk.Button(
            container, text="Ulangi Kuis",
            font=("Segoe UI", 11, "bold"), bg="#4263EB",
            fg="white", activebackground="#3451C6",
            activeforeground="white", relief=tk.FLAT,
            padx=25, pady=12, command=self.ulangi_kuis,
            cursor="hand2"
        ).pack(pady=22)

        tk.Button(
            container, text="Keluar", font=("Segoe UI", 10),
            bg="#E2E8F0", fg="#334155", relief=tk.FLAT,
            padx=25, pady=9, command=self.root.destroy,
            cursor="hand2"
        ).pack()

    def ulangi_kuis(self):
        self.batalkan_timer()
        self.batalkan_feedback()
        self.indeks_soal = 0
        self.skor = 0
        self.jawaban_pengguna = [None] * len(self.SOAL)
        self.status_soal = ["belum"] * len(self.SOAL)
        # Setiap soal punya timer sendiri; waktu tidak di-reset saat navigasi.
        self.waktu_per_soal = [self.DURASI_SOAL] * len(self.SOAL)
        self.sisa_waktu = self.DURASI_SOAL
        self.sedang_feedback = False
        self.sudah_selesai = False

        for widget in self.root.winfo_children():
            widget.destroy()

        self.buat_interface()
        self.tampilkan_soal()
        self.jalankan_timer()

    def konfirmasi_keluar(self):
        if messagebox.askyesno("Keluar dari kuis", "Yakin ingin menutup aplikasi?"):
            self.batalkan_timer()
            self.batalkan_feedback()
            self.root.destroy()

    def jalankan(self):
        self.root.mainloop()


if __name__ == "__main__":
    aplikasi = QuizInteraktif()
    aplikasi.jalankan()
