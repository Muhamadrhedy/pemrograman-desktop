
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random


# =========================================================
# HELPER
# =========================================================

def interpolate_color(start, end, factor):
    """Menghasilkan warna di antara dua warna HEX."""
    start = start.lstrip("#")
    end = end.lstrip("#")

    r1, g1, b1 = int(start[0:2], 16), int(start[2:4], 16), int(start[4:6], 16)
    r2, g2, b2 = int(end[0:2], 16), int(end[2:4], 16), int(end[4:6], 16)

    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)

    return f"#{r:02x}{g:02x}{b:02x}"


# =========================================================
# PRAKTIKUM 3.1 - ANIMATION APP
# =========================================================

class AnimatedApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.root = parent.winfo_toplevel()

        self.animation_running = False
        self.progress_value = 0
        self.slide_running = False
        self.fade_running = False
        self.fade_visible = True

        self.dark_bg = "#2d2d2d"
        self.dark_fg = "#ffffff"

        self._setup_styles()
        self._buat_interface()

    def _setup_styles(self):
        self.style = ttk.Style()

        self.style.configure(
            "Animation.TFrame",
            background="#2d2d2d"
        )

        self.style.configure(
            "Animation.TLabel",
            background="#2d2d2d",
            foreground="#ffffff",
            font=("Arial", 11)
        )

        self.style.configure(
            "AnimationTitle.TLabel",
            background="#2d2d2d",
            foreground="#00ff88",
            font=("Arial", 16, "bold")
        )

        self.style.configure(
            "Animated.TButton",
            padding=(15, 8),
            font=("Arial", 10, "bold")
        )

        self.style.configure(
            "Animation.TLabelframe",
            background="#2d2d2d",
            foreground="#ffffff"
        )

        self.style.configure(
            "Animation.TLabelframe.Label",
            background="#2d2d2d",
            foreground="#00ff88",
            font=("Arial", 10, "bold")
        )

        self.style.configure(
            "Animation.Horizontal.TProgressbar",
            troughcolor="#444444",
            background="#00ff88"
        )

    def _buat_interface(self):
        self.configure(style="Animation.TFrame")
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header = ttk.Frame(self, style="Animation.TFrame")
        header.pack(fill="x", pady=(0, 20))

        ttk.Label(
            header,
            text="🎬 Animation Demo",
            style="AnimationTitle.TLabel"
        ).pack()

        # Progress section
        progress_frame = ttk.LabelFrame(
            self,
            text="Progress Animation",
            padding=15,
            style="Animation.TLabelframe"
        )
        progress_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            progress_frame,
            text="Animated Progress Bar:",
            style="Animation.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode="determinate",
            maximum=100,
            style="Animation.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill="x", pady=(0, 10))

        self.progress_label = ttk.Label(
            progress_frame,
            text="0%",
            style="Animation.TLabel"
        )
        self.progress_label.pack(anchor="e")

        controls = ttk.Frame(progress_frame, style="Animation.TFrame")
        controls.pack(fill="x", pady=5)

        ttk.Button(
            controls,
            text="Start Animation",
            style="Animated.TButton",
            command=self.start_progress_animation
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="Stop Animation",
            style="Animated.TButton",
            command=self.stop_animation
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="Reset",
            style="Animated.TButton",
            command=self.reset_progress
        ).pack(side="left", padx=5)

        # Sliding panel
        slide_frame = ttk.LabelFrame(
            self,
            text="Sliding Panel",
            padding=15,
            style="Animation.TLabelframe"
        )
        slide_frame.pack(fill="x", pady=(0, 15))

        self.slide_container = tk.Frame(
            slide_frame,
            bg="#1a1a1a",
            height=130
        )
        self.slide_container.pack(fill="x", pady=(0, 10))
        self.slide_container.pack_propagate(False)

        self.sliding_panel = tk.Frame(
            self.slide_container,
            bg="#3a3a3a"
        )

        tk.Label(
            self.sliding_panel,
            text="🎯 Sliding Panel Content",
            bg="#3a3a3a",
            fg="#00ff88",
            font=("Arial", 14, "bold")
        ).pack(pady=(25, 10))

        tk.Label(
            self.sliding_panel,
            text="Panel ini dapat bergerak masuk dan keluar",
            bg="#3a3a3a",
            fg="white",
            font=("Arial", 10)
        ).pack()

        slide_controls = ttk.Frame(slide_frame, style="Animation.TFrame")
        slide_controls.pack(fill="x")

        ttk.Button(
            slide_controls,
            text="Slide In",
            command=self.slide_in
        ).pack(side="left", padx=5)

        ttk.Button(
            slide_controls,
            text="Slide Out",
            command=self.slide_out
        ).pack(side="left", padx=5)

        # Fade section
        self.fade_frame = ttk.LabelFrame(
            self,
            text="Fade Animation",
            padding=15,
            style="Animation.TLabelframe"
        )
        self.fade_frame.pack(fill="both", expand=True)

        self.fade_content = tk.Frame(
            self.fade_frame,
            bg="#2d2d2d",
            height=90
        )
        self.fade_content.pack(fill="both", expand=True, pady=10)

        self.fade_title = tk.Label(
            self.fade_content,
            text="✨ Fade Content",
            bg="#2d2d2d",
            fg="#00ff88",
            font=("Arial", 16, "bold")
        )
        self.fade_title.pack(pady=(15, 5))

        self.fade_description = tk.Label(
            self.fade_content,
            text="Content ini dapat fade in dan fade out",
            bg="#2d2d2d",
            fg="#ffffff",
            font=("Arial", 10)
        )
        self.fade_description.pack()

        fade_controls = ttk.Frame(self.fade_frame, style="Animation.TFrame")
        fade_controls.pack(fill="x")

        ttk.Button(
            fade_controls,
            text="Fade Out",
            command=self.fade_out
        ).pack(side="left", padx=5)

        ttk.Button(
            fade_controls,
            text="Fade In",
            command=self.fade_in
        ).pack(side="left", padx=5)

    # ---------------- Progress Animation ----------------

    def start_progress_animation(self):
        if self.animation_running or self.progress_value >= 100:
            return

        self.animation_running = True
        self._animate_progress()

    def _animate_progress(self):
        if not self.animation_running:
            return

        if self.progress_value < 100:
            self.progress_value += 1

            self.progress_bar["value"] = self.progress_value
            self.progress_label.config(
                text=f"{self.progress_value}%"
            )

            self.after(30, self._animate_progress)
        else:
            self.animation_running = False

    def stop_animation(self):
        self.animation_running = False

    def reset_progress(self):
        self.animation_running = False
        self.progress_value = 0
        self.progress_bar["value"] = 0
        self.progress_label.config(text="0%")

    # ---------------- Sliding Animation ----------------

    def slide_in(self):
        if self.slide_running:
            return

        self.slide_running = True
        self._animate_slide(0, 30, 10)

    def slide_out(self):
        if self.slide_running:
            return

        self.slide_running = True
        self._animate_slide(30, 0, -10)

    def _animate_slide(self, step, end, direction):
        if step == end:
            self.slide_running = False
            return

        x = -300 + step * 10

        self.sliding_panel.place(
            x=x,
            y=0,
            width=300,
            height=130
        )

        next_step = step + (1 if direction > 0 else -1)
        self.after(
            15,
            lambda: self._animate_slide(next_step, end, direction)
        )

    # ---------------- Fade Animation ----------------

    def fade_out(self):
        if self.fade_running or not self.fade_visible:
            return

        self.fade_running = True
        self._animate_fade(0, 20)

    def fade_in(self):
        if self.fade_running or self.fade_visible:
            return

        self.fade_running = True
        self.fade_content.pack(fill="both", expand=True, pady=10)
        self._animate_fade(20, 0)

    def _animate_fade(self, step, end):
        factor = step / 20

        bg = interpolate_color("#111111", "#2d2d2d", factor)
        title_fg = interpolate_color("#111111", "#00ff88", factor)
        desc_fg = interpolate_color("#111111", "#ffffff", factor)

        self.fade_content.configure(bg=bg)
        self.fade_title.configure(bg=bg, fg=title_fg)
        self.fade_description.configure(bg=bg, fg=desc_fg)

        if step == end:
            self.fade_running = False

            if end == 20:
                self.fade_content.pack_forget()
                self.fade_visible = False
            else:
                self.fade_visible = True

            return

        next_step = step + (1 if end > step else -1)

        self.after(
            30,
            lambda: self._animate_fade(next_step, end)
        )


# =========================================================
# PRAKTIKUM 3.2 - INTERACTIVE DASHBOARD
# =========================================================

class InteractiveDashboard(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.root = parent.winfo_toplevel()

        self.is_running = False
        self.monitor_job = None

        self.cpu_data = []
        self.memory_data = []
        self.network_data = []

        self.max_data_points = 50

        self.current_cpu = 0
        self.current_memory = 0
        self.current_network = 0

        self.total_requests = 0
        self.active_users = 0

        self._setup_styles()
        self._buat_interface()

    def _setup_styles(self):
        self.style = ttk.Style()

        self.style.configure(
            "Dashboard.TFrame",
            background="#1e2328"
        )

        self.style.configure(
            "Card.TFrame",
            background="#252a31",
            relief="raised",
            borderwidth=1
        )

        self.style.configure(
            "Dashboard.TLabel",
            background="#1e2328",
            foreground="#ffffff",
            font=("Arial", 10)
        )

        self.style.configure(
            "DashboardTitle.TLabel",
            background="#1e2328",
            foreground="#00d4ff",
            font=("Arial", 16, "bold")
        )

        self.style.configure(
            "Metric.TLabel",
            background="#252a31",
            foreground="#00ff88",
            font=("Arial", 20, "bold")
        )

        self.style.configure(
            "MetricLabel.TLabel",
            background="#252a31",
            foreground="#ffffff",
            font=("Arial", 10)
        )

        self.style.configure(
            "Control.TButton",
            padding=(12, 8),
            font=("Arial", 9, "bold")
        )

    def _buat_interface(self):
        self.configure(style="Dashboard.TFrame")
        self.pack(fill="both", expand=True, padx=15, pady=15)

        # Header
        header = ttk.Frame(self, style="Dashboard.TFrame")
        header.pack(fill="x", pady=(0, 20))

        ttk.Label(
            header,
            text="📊 System Dashboard",
            style="DashboardTitle.TLabel"
        ).pack(side="left")

        self.time_label = ttk.Label(
            header,
            text="",
            style="Dashboard.TLabel"
        )
        self.time_label.pack(side="right", padx=10)

        self.status_label = ttk.Label(
            header,
            text="● Stopped",
            style="Dashboard.TLabel"
        )
        self.status_label.pack(side="right")

        # Metrics cards
        metrics_frame = ttk.Frame(self, style="Dashboard.TFrame")
        metrics_frame.pack(fill="x", pady=(0, 15))

        self.cpu_metric, self.cpu_progress = self._create_metric_card(
            metrics_frame, "CPU Usage", "0%"
        )

        self.memory_metric, self.memory_progress = self._create_metric_card(
            metrics_frame, "Memory Usage", "0%"
        )

        self.network_metric, self.network_progress = self._create_metric_card(
            metrics_frame, "Network I/O", "0 MB/s"
        )

        # Statistics cards
        stats_frame = ttk.Frame(self, style="Dashboard.TFrame")
        stats_frame.pack(fill="x", pady=(0, 15))

        self.requests_metric = self._create_stat_card(
            stats_frame, "Total Requests", "0"
        )

        self.users_metric = self._create_stat_card(
            stats_frame, "Active Users", "0"
        )

        # Monitoring chart
        chart_frame = ttk.LabelFrame(
            self,
            text="Real-time Monitoring",
            padding=10
        )
        chart_frame.pack(fill="both", expand=True, pady=(0, 15))

        self.chart_text = tk.Text(
            chart_frame,
            height=12,
            bg="#0f1419",
            fg="#00ff88",
            insertbackground="white",
            font=("Consolas", 9),
            state="disabled"
        )
        self.chart_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            chart_frame,
            orient="vertical",
            command=self.chart_text.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.chart_text.configure(
            yscrollcommand=scrollbar.set
        )

        # Controls
        controls = ttk.Frame(self, style="Dashboard.TFrame")
        controls.pack(fill="x")

        ttk.Button(
            controls,
            text="▶ Start Monitoring",
            style="Control.TButton",
            command=self.start_monitoring
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="⏸ Stop Monitoring",
            style="Control.TButton",
            command=self.stop_monitoring
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="🗑 Clear Data",
            style="Control.TButton",
            command=self.clear_data
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="📊 Generate Report",
            style="Control.TButton",
            command=self.generate_report
        ).pack(side="right", padx=5)

        self._update_time()

    def _create_metric_card(self, parent, title, initial):
        card = ttk.Frame(
            parent,
            style="Card.TFrame",
            padding=15
        )
        card.pack(side="left", fill="both", expand=True, padx=5)

        ttk.Label(
            card,
            text=title,
            style="MetricLabel.TLabel"
        ).pack()

        metric = ttk.Label(
            card,
            text=initial,
            style="Metric.TLabel"
        )
        metric.pack(pady=5)

        progress = ttk.Progressbar(
            card,
            maximum=100,
            mode="determinate"
        )
        progress.pack(fill="x", pady=5)

        return metric, progress

    def _create_stat_card(self, parent, title, initial):
        card = ttk.Frame(
            parent,
            style="Card.TFrame",
            padding=15
        )
        card.pack(side="left", fill="both", expand=True, padx=5)

        ttk.Label(
            card,
            text=title,
            style="MetricLabel.TLabel"
        ).pack()

        metric = ttk.Label(
            card,
            text=initial,
            style="Metric.TLabel"
        )
        metric.pack(pady=5)

        return metric

    # ---------------- Time ----------------

    def _update_time(self):
        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.time_label.config(text=current_time)

        self.after(1000, self._update_time)

    # ---------------- Monitoring ----------------

    def start_monitoring(self):
        if self.is_running:
            return

        self.is_running = True

        self.status_label.config(
            text="● Running",
            foreground="#00ff88"
        )

        self._monitoring_loop()

    def stop_monitoring(self):
        self.is_running = False

        if self.monitor_job:
            self.after_cancel(self.monitor_job)
            self.monitor_job = None

        self.status_label.config(
            text="● Stopped",
            foreground="#ff4444"
        )

    def _monitoring_loop(self):
        if not self.is_running:
            return

        # Simulasi data monitoring
        self.current_cpu = random.randint(10, 90)
        self.current_memory = random.randint(20, 80)
        self.current_network = random.uniform(0.1, 10.0)

        self.total_requests += random.randint(1, 5)
        self.active_users = random.randint(50, 200)

        # Simpan data
        self.cpu_data.append(self.current_cpu)
        self.memory_data.append(self.current_memory)
        self.network_data.append(self.current_network)

        # Batasi jumlah data
        if len(self.cpu_data) > self.max_data_points:
            self.cpu_data.pop(0)
            self.memory_data.pop(0)
            self.network_data.pop(0)

        self._update_metrics()
        self._update_chart()

        # Update berikutnya setelah 1 detik
        self.monitor_job = self.after(
            1000,
            self._monitoring_loop
        )

    # ---------------- Update Metrics ----------------

    def _update_metrics(self):
        self.cpu_metric.config(
            text=f"{self.current_cpu}%"
        )
        self.cpu_progress["value"] = self.current_cpu

        self.memory_metric.config(
            text=f"{self.current_memory}%"
        )
        self.memory_progress["value"] = self.current_memory

        self.network_metric.config(
            text=f"{self.current_network:.1f} MB/s"
        )
        self.network_progress["value"] = min(
            self.current_network * 10, 100
        )

        self.requests_metric.config(
            text=str(self.total_requests)
        )

        self.users_metric.config(
            text=str(self.active_users)
        )

    # ---------------- Update Chart ----------------

    def _update_chart(self):
        timestamp = datetime.now().strftime("%H:%M:%S")

        cpu_bar = "█" * (self.current_cpu // 5)
        memory_bar = "█" * (self.current_memory // 5)
        network_bar = "█" * min(
            int(self.current_network), 20
        )

        chart_line = (
            f"[{timestamp}] "
            f"CPU: {cpu_bar:<20} {self.current_cpu}% | "
            f"MEM: {memory_bar:<20} {self.current_memory}% | "
            f"NET: {network_bar:<20} "
            f"{self.current_network:.1f} MB/s\n"
        )

        self.chart_text.config(state="normal")
        self.chart_text.insert("end", chart_line)
        self.chart_text.see("end")
        self.chart_text.config(state="disabled")

    # ---------------- Clear Data ----------------

    def clear_data(self):
        self.cpu_data.clear()
        self.memory_data.clear()
        self.network_data.clear()

        self.total_requests = 0
        self.active_users = 0

        self.current_cpu = 0
        self.current_memory = 0
        self.current_network = 0

        self._update_metrics()

        self.chart_text.config(state="normal")
        self.chart_text.delete("1.0", "end")
        self.chart_text.config(state="disabled")

    # ---------------- Generate Report ----------------

    def generate_report(self):
        if not self.cpu_data:
            self.chart_text.config(state="normal")
            self.chart_text.insert(
                "end",
                "\nBelum ada data untuk dibuat laporan.\n"
            )
            self.chart_text.config(state="disabled")
            return

        avg_cpu = sum(self.cpu_data) / len(self.cpu_data)
        avg_memory = sum(self.memory_data) / len(self.memory_data)
        avg_network = sum(self.network_data) / len(self.network_data)

        report = (
            "\n" + "=" * 60 + "\n"
            "SYSTEM PERFORMANCE REPORT\n"
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            + "=" * 60 + "\n"
            f"Average CPU Usage: {avg_cpu:.1f}%\n"
            f"Average Memory Usage: {avg_memory:.1f}%\n"
            f"Average Network I/O: {avg_network:.1f} MB/s\n"
            f"Total Requests: {self.total_requests}\n"
            f"Current Active Users: {self.active_users}\n"
            f"Data Points Collected: {len(self.cpu_data)}\n"
            + "=" * 60 + "\n"
        )

        self.chart_text.config(state="normal")
        self.chart_text.insert("end", report)
        self.chart_text.see("end")
        self.chart_text.config(state="disabled")


# =========================================================
# MAIN APPLICATION
# =========================================================

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Praktikum 3 - Animation & Dashboard")
        self.root.geometry("1000x750")
        self.root.minsize(800, 600)
        self.root.configure(bg="#1a1a1a")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self._buat_interface()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self._on_close
        )

    def _buat_interface(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        animation_tab = ttk.Frame(notebook)
        dashboard_tab = ttk.Frame(notebook)

        notebook.add(
            animation_tab,
            text="3.1 Animation"
        )

        notebook.add(
            dashboard_tab,
            text="3.2 Dashboard"
        )

        self.animation_app = AnimatedApp(animation_tab)
        self.dashboard_app = InteractiveDashboard(dashboard_tab)

    def _on_close(self):
        self.dashboard_app.stop_monitoring()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
