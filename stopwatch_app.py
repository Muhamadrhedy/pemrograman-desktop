import tkinter as tk
import math
import time


class StopwatchApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Stopwatch dengan Animasi")
        self.window.geometry("600x700")
        self.window.minsize(500, 600)
        self.window.configure(bg="black")

        # Variabel stopwatch
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.is_running = False
        self.timer_job = None

        # Variabel animasi
        self.animation_job = None
        self.rotation_angle = 0

        # Variabel lap
        self.lap_times = []
        self.lap_count = 0

        self.buat_interface()
        self.start_animation()
        self.window.protocol("WM_DELETE_WINDOW", self.tutup_aplikasi)

    def buat_interface(self):
        # Display waktu
        time_frame = tk.Frame(self.window, bg="black")
        time_frame.pack(pady=(20, 5))

        self.time_label = tk.Label(
            time_frame,
            text="00:00:00",
            font=("Courier", 42, "bold"),
            fg="lime",
            bg="black",
        )
        self.time_label.pack()

        self.ms_label = tk.Label(
            time_frame,
            text="000",
            font=("Courier", 20),
            fg="yellow",
            bg="black",
        )
        self.ms_label.pack()

        # Canvas jam analog
        self.canvas = tk.Canvas(
            self.window,
            width=300,
            height=300,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack(pady=10)

        self.canvas.create_oval(
            50, 50, 250, 250,
            outline="white",
            width=3,
            tags="outer_circle",
        )

        self.buat_penanda_waktu()

        self.jarum_detik = self.canvas.create_line(
            150, 150, 150, 80,
            fill="red",
            width=3,
            tags="second_hand",
        )

        self.canvas.create_oval(
            145, 145, 155, 155,
            fill="white",
            outline="white",
        )

        # Tombol kontrol
        control_frame = tk.Frame(self.window, bg="black")
        control_frame.pack(pady=10)

        self.start_stop_btn = tk.Button(
            control_frame,
            text="START",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            activebackground="#16803c",
            activeforeground="white",
            width=9,
            command=self.toggle_stopwatch,
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=6)

        self.reset_btn = tk.Button(
            control_frame,
            text="RESET",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            width=9,
            command=self.reset_stopwatch,
        )
        self.reset_btn.pack(side=tk.LEFT, padx=6)

        self.lap_btn = tk.Button(
            control_frame,
            text="LAP",
            font=("Arial", 12, "bold"),
            bg="blue",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=9,
            command=self.record_lap,
            state=tk.DISABLED,
        )
        self.lap_btn.pack(side=tk.LEFT, padx=6)

        # Daftar lap
        lap_frame = tk.LabelFrame(
            self.window,
            text="Lap Times",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="black",
            labelanchor="nw",
        )
        lap_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 15))

        self.lap_listbox = tk.Listbox(
            lap_frame,
            font=("Courier", 10),
            bg="#111111",
            fg="lime",
            selectbackground="gray",
            selectforeground="white",
            height=6,
        )
        self.lap_listbox.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    def buat_penanda_waktu(self):
        """Membuat 60 penanda waktu di sekeliling lingkaran."""
        center_x, center_y = 150, 150
        radius = 90

        for i in range(60):
            angle = math.radians(i * 6 - 90)

            if i % 5 == 0:
                inner_radius = radius - 15
                width = 3
                color = "white"
            else:
                inner_radius = radius - 8
                width = 1
                color = "gray"

            x1 = center_x + radius * math.cos(angle)
            y1 = center_y + radius * math.sin(angle)
            x2 = center_x + inner_radius * math.cos(angle)
            y2 = center_y + inner_radius * math.sin(angle)

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=width,
            )

    def toggle_stopwatch(self):
        if self.is_running:
            self.stop_stopwatch()
        else:
            self.start_stopwatch()

    def start_stopwatch(self):
        if self.is_running:
            return

        self.is_running = True
        self.start_time = time.perf_counter() - self.elapsed_time
        self.start_stop_btn.config(text="STOP", bg="red")
        self.lap_btn.config(state=tk.NORMAL)
        self.update_time()

    def stop_stopwatch(self):
        self.is_running = False
        self.start_stop_btn.config(text="START", bg="green")
        self.lap_btn.config(state=tk.DISABLED)

        if self.timer_job is not None:
            self.window.after_cancel(self.timer_job)
            self.timer_job = None

    def reset_stopwatch(self):
        self.stop_stopwatch()
        self.elapsed_time = 0.0
        self.time_label.config(text="00:00:00")
        self.ms_label.config(text="000")
        self.lap_times.clear()
        self.lap_count = 0
        self.lap_listbox.delete(0, tk.END)
        self.update_second_hand(0)

    def record_lap(self):
        if not self.is_running:
            return

        # Ambil waktu terkini agar catatan lap akurat
        current_time = time.perf_counter() - self.start_time
        self.elapsed_time = current_time

        if self.lap_times:
            lap_time = current_time - self.lap_times[-1][1]
        else:
            lap_time = current_time

        self.lap_count += 1
        self.lap_times.append((self.lap_count, current_time, lap_time))

        total_formatted = self.format_time(current_time)
        lap_formatted = self.format_time(lap_time)
        self.lap_listbox.insert(
            tk.END,
            f"Lap {self.lap_count:2d}: {lap_formatted}.{int((lap_time % 1) * 1000):03d} "
            f"(Total: {total_formatted}.{int((current_time % 1) * 1000):03d})",
        )
        self.lap_listbox.see(tk.END)

    def update_time(self):
        if not self.is_running:
            return

        self.elapsed_time = time.perf_counter() - self.start_time

        self.time_label.config(text=self.format_time(self.elapsed_time))
        milliseconds = int((self.elapsed_time % 1) * 1000)
        self.ms_label.config(text=f"{milliseconds:03d}")

        self.update_second_hand(self.elapsed_time % 60)
        self.timer_job = self.window.after(10, self.update_time)

    @staticmethod
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def update_second_hand(self, seconds):
        angle = math.radians(seconds * 6 - 90)
        center_x, center_y = 150, 150
        length = 70
        end_x = center_x + length * math.cos(angle)
        end_y = center_y + length * math.sin(angle)

        self.canvas.coords(
            self.jarum_detik,
            center_x, center_y, end_x, end_y,
        )

    def start_animation(self):
        self.animate_background()

    def animate_background(self):
        self.rotation_angle = (self.rotation_angle + 1) % 360

        if self.is_running:
            intensity = int(
                127 + 127 * math.sin(math.radians(self.rotation_angle * 4))
            )
            color = f"#{intensity:02x}0000"
        else:
            color = "white"

        self.canvas.itemconfig("outer_circle", outline=color)
        self.animation_job = self.window.after(50, self.animate_background)

    def tutup_aplikasi(self):
        for job in (self.timer_job, self.animation_job):
            if job is not None:
                try:
                    self.window.after_cancel(job)
                except tk.TclError:
                    pass
        self.window.destroy()

    def jalankan(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = StopwatchApp()
    app.jalankan()
