
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class PerbandinganWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        # Variabel Tkinter standar
        self.nama_tk = tk.StringVar()
        self.gender_tk = tk.StringVar(value="Laki-laki")
        self.hobi_tk = {
            "membaca": tk.BooleanVar(),
            "olahraga": tk.BooleanVar(),
            "musik": tk.BooleanVar()
        }

        # Variabel ttk
        self.nama_ttk = tk.StringVar()
        self.gender_ttk = tk.StringVar(value="Laki-laki")
        self.hobi_ttk = {
            "membaca": tk.BooleanVar(),
            "olahraga": tk.BooleanVar(),
            "musik": tk.BooleanVar()
        }

        self.buat_interface()

    def buat_interface(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", height=70)
        header.pack(fill="x", pady=(0, 10))
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Perbandingan Widget Tkinter vs ttk",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(expand=True)

        # Container utama
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # Frame Tkinter standar
        tk_frame = tk.LabelFrame(
            container,
            text="Widget Tkinter Standar",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        tk_frame.pack(
            side="left", fill="both", expand=True,
            padx=(0, 5), pady=5
        )

        # Input nama
        tk.Label(
            tk_frame, text="Nama:",
            font=("Arial", 10), bg="#f0f0f0"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.tk_entry = tk.Entry(
            tk_frame, textvariable=self.nama_tk,
            font=("Arial", 10)
        )
        self.tk_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Gender
        tk.Label(
            tk_frame, text="Gender:",
            font=("Arial", 10), bg="#f0f0f0"
        ).pack(anchor="w", padx=10)

        tk.OptionMenu(
            tk_frame, self.gender_tk,
            "Laki-laki", "Perempuan"
        ).pack(fill="x", padx=10, pady=(0, 10))

        # Hobi
        tk.Label(
            tk_frame, text="Hobi:",
            font=("Arial", 10), bg="#f0f0f0"
        ).pack(anchor="w", padx=10)

        for hobi, var in self.hobi_tk.items():
            tk.Checkbutton(
                tk_frame,
                text=hobi.capitalize(),
                variable=var,
                font=("Arial", 9),
                bg="#f0f0f0"
            ).pack(anchor="w", padx=20)

        # Button
        tk.Button(
            tk_frame,
            text="Submit (Tkinter)",
            command=self.submit_tk,
            font=("Arial", 10),
            bg="#3498db",
            fg="white"
        ).pack(pady=20, padx=10)

        # Frame ttk
        ttk_frame = ttk.LabelFrame(
            container,
            text="Widget ttk (Themed)",
            padding=10
        )
        ttk_frame.pack(
            side="right", fill="both", expand=True,
            padx=(5, 0), pady=5
        )

        # Input nama
        ttk.Label(
            ttk_frame, text="Nama:"
        ).pack(anchor="w", pady=(0, 2))

        self.ttk_entry = ttk.Entry(
            ttk_frame, textvariable=self.nama_ttk
        )
        self.ttk_entry.pack(fill="x", pady=(0, 10))

        # Gender
        ttk.Label(
            ttk_frame, text="Gender:"
        ).pack(anchor="w")

        self.ttk_combo = ttk.Combobox(
            ttk_frame,
            textvariable=self.gender_ttk,
            values=["Laki-laki", "Perempuan"],
            state="readonly"
        )
        self.ttk_combo.pack(fill="x", pady=(0, 10))

        # Hobi
        ttk.Label(
            ttk_frame, text="Hobi:"
        ).pack(anchor="w")

        for hobi, var in self.hobi_ttk.items():
            ttk.Checkbutton(
                ttk_frame,
                text=hobi.capitalize(),
                variable=var
            ).pack(anchor="w", padx=20)

        # Button
        ttk.Button(
            ttk_frame,
            text="Submit (ttk)",
            command=self.submit_ttk
        ).pack(pady=20)

    def submit_tk(self):
        hobi = [
            nama for nama, var in self.hobi_tk.items()
            if var.get()
        ]

        print("\n=== TKINTER STANDAR ===")
        print("Nama:", self.nama_tk.get())
        print("Gender:", self.gender_tk.get())
        print("Hobi:", hobi)

    def submit_ttk(self):
        hobi = [
            nama for nama, var in self.hobi_ttk.items()
            if var.get()
        ]

        print("\n=== TTK ===")
        print("Nama:", self.nama_ttk.get())
        print("Gender:", self.gender_ttk.get())
        print("Hobi:", hobi)


class ThemeSwitcher(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent, padding=20)

        self.style = style
        self.current_theme = tk.StringVar(
            value=self.style.theme_use()
        )

        self.buat_interface()
        self.setup_themes()

    def buat_interface(self):
        # Header
        ttk.Label(
            self,
            text="Theme Switcher Demo",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))

        # Theme selection
        theme_frame = ttk.LabelFrame(
            self,
            text="Pilih Theme",
            padding=10
        )
        theme_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            theme_frame,
            text="Theme:"
        ).pack(anchor="w")

        self.theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.current_theme,
            values=self.style.theme_names(),
            state="readonly"
        )
        self.theme_combo.pack(fill="x", pady=(5, 10))

        self.theme_combo.bind(
            "<<ComboboxSelected>>",
            self.change_theme
        )

        # Demo widgets
        demo_frame = ttk.LabelFrame(
            self,
            text="Demo Widgets",
            padding=10
        )
        demo_frame.pack(fill="both", expand=True)

        # Entry
        ttk.Label(
            demo_frame,
            text="Entry Widget:"
        ).pack(anchor="w")

        self.demo_entry = ttk.Entry(demo_frame)
        self.demo_entry.pack(fill="x", pady=(5, 10))
        self.demo_entry.insert(0, "Contoh text...")

        # Buttons
        button_frame = ttk.Frame(demo_frame)
        button_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            button_frame,
            text="Normal Button"
        ).pack(side="left", padx=(0, 5))

        ttk.Button(
            button_frame,
            text="Disabled Button",
            state="disabled"
        ).pack(side="left")

        # Progressbar
        ttk.Label(
            demo_frame,
            text="Progress Bar:"
        ).pack(anchor="w")

        self.progress = ttk.Progressbar(
            demo_frame,
            mode="determinate",
            value=70
        )
        self.progress.pack(fill="x", pady=(5, 10))

        # Scale
        ttk.Label(
            demo_frame,
            text="Scale Widget:"
        ).pack(anchor="w")

        self.scale = ttk.Scale(
            demo_frame,
            from_=0,
            to=100,
            orient="horizontal"
        )
        self.scale.pack(fill="x", pady=(5, 10))
        self.scale.set(50)

    def setup_themes(self):
        available_themes = self.style.theme_names()
        print("Available themes:", available_themes)

    def change_theme(self, event=None):
        selected_theme = self.current_theme.get()

        try:
            self.style.theme_use(selected_theme)
            print("Theme changed to:", selected_theme)

        except tk.TclError as e:
            print("Error changing theme:", e)


class Aplikasi:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Praktikum Tkinter - Widget & Theme")
        self.root.geometry("850x650")
        self.root.minsize(700, 550)

        # Style global ttk
        self.style = ttk.Style()

        # Notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1
        tab_perbandingan = PerbandinganWidget(notebook)
        notebook.add(
            tab_perbandingan,
            text="Perbandingan Widget"
        )

        # Tab 2
        tab_theme = ThemeSwitcher(notebook, self.style)
        notebook.add(
            tab_theme,
            text="Theme Switcher"
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Aplikasi()
    app.run()
