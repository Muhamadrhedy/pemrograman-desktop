
import tkinter as tk
from tkinter import ttk


class CustomStyleApp(ttk.Frame):

    def __init__(self, parent, style):
        super().__init__(parent)

        self.style = style

        self.setup_custom_styles()
        self.buat_interface()

    def setup_custom_styles(self):

        # Custom button
        self.style.configure(
            "Custom.TButton",
            background="#3498db",
            foreground="white",
            borderwidth=0,
            focuscolor="none",
            padding=(20, 10)
        )

        self.style.map(
            "Custom.TButton",
            background=[
                ("active", "#2980b9"),
                ("pressed", "#21618c")
            ]
        )

        # Custom entry
        self.style.configure(
            "Custom.TEntry",
            fieldbackground="#ecf0f1",
            borderwidth=2,
            insertcolor="#2c3e50",
            padding=(10, 8)
        )

        self.style.map(
            "Custom.TEntry",
            focuscolor=[("focus", "#3498db")]
        )

        # Custom label
        self.style.configure(
            "Title.TLabel",
            background="#2c3e50",
            foreground="#ecf0f1",
            font=("Arial", 18, "bold")
        )

        self.style.configure(
            "Subtitle.TLabel",
            background="#2c3e50",
            foreground="#bdc3c7",
            font=("Arial", 12)
        )

    def buat_interface(self):

        self.configure(style="Main.TFrame")

        main_frame = ttk.Frame(
            self,
            style="Main.TFrame",
            padding=20
        )
        main_frame.pack(fill="both", expand=True)

        # Header
        header_frame = ttk.Frame(
            main_frame,
            style="Main.TFrame"
        )
        header_frame.pack(fill="x", pady=(0, 30))

        ttk.Label(
            header_frame,
            text="Custom Styling Demo",
            style="Title.TLabel"
        ).pack()

        ttk.Label(
            header_frame,
            text="Aplikasi dengan styling kustom menggunakan ttk.Style",
            style="Subtitle.TLabel"
        ).pack(pady=(5, 0))

        # Form
        form_frame = ttk.LabelFrame(
            main_frame,
            text="Form Input",
            padding=20
        )
        form_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            form_frame,
            text="Nama Lengkap:"
        ).pack(anchor="w", pady=(0, 5))

        self.nama_entry = ttk.Entry(
            form_frame,
            style="Custom.TEntry",
            width=40
        )
        self.nama_entry.pack(fill="x", pady=(0, 15))

        ttk.Label(
            form_frame,
            text="Email:"
        ).pack(anchor="w", pady=(0, 5))

        self.email_entry = ttk.Entry(
            form_frame,
            style="Custom.TEntry",
            width=40
        )
        self.email_entry.pack(fill="x", pady=(0, 15))

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(
            button_frame,
            text="Submit Data",
            style="Custom.TButton",
            command=self.submit_data
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            button_frame,
            text="Reset Form",
            style="Custom.TButton",
            command=self.reset_form
        ).pack(side="left")

        # Result
        self.result_frame = ttk.LabelFrame(
            main_frame,
            text="Hasil Input",
            padding=20
        )
        self.result_frame.pack(fill="both", expand=True)

        self.result_text = tk.Text(
            self.result_frame,
            height=8,
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Consolas", 10),
            wrap="word"
        )
        self.result_text.pack(fill="both", expand=True)

    def submit_data(self):

        nama = self.nama_entry.get().strip()
        email = self.email_entry.get().strip()

        if nama and email:

            result = (
                "Data berhasil disubmit:\n"
                f"Nama: {nama}\n"
                f"Email: {email}\n"
                + "=" * 40 + "\n"
            )

        else:

            result = (
                "Error: Semua field harus diisi!\n"
                + "=" * 40 + "\n"
            )

        self.result_text.insert("end", result)
        self.result_text.see("end")

    def reset_form(self):

        self.nama_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.result_text.delete("1.0", "end")



class ResponsiveApp(ttk.Frame):

    def __init__(self, parent, style):

        super().__init__(parent)

        self.style = style

        self.current_width = 800
        self.current_height = 600

        self.setup_styles()
        self.buat_interface()

        self.bind("<Configure>", self.on_frame_resize)

    def setup_styles(self):

        self.style.configure(
            "Desktop.TLabel",
            font=("Arial", 12),
            padding=(10, 5)
        )

        self.style.configure(
            "Tablet.TLabel",
            font=("Arial", 10),
            padding=(8, 4)
        )

        self.style.configure(
            "Mobile.TLabel",
            font=("Arial", 9),
            padding=(5, 3)
        )

        self.style.configure(
            "Desktop.TButton",
            padding=(15, 8),
            font=("Arial", 11)
        )

        self.style.configure(
            "Tablet.TButton",
            padding=(12, 6),
            font=("Arial", 10)
        )

        self.style.configure(
            "Mobile.TButton",
            padding=(8, 4),
            font=("Arial", 9)
        )

    def buat_interface(self):

        # Canvas dan scrollbar
        self.canvas = tk.Canvas(
            self,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            self.on_canvas_resize
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        # Header
        self.header_frame = ttk.Frame(
            self.scrollable_frame
        )
        self.header_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.title_label = ttk.Label(
            self.header_frame,
            text="Responsive Design Demo",
            style="Desktop.TLabel"
        )
        self.title_label.pack()

        self.size_label = ttk.Label(
            self.header_frame,
            text="Window Size: 800x600",
            style="Desktop.TLabel"
        )
        self.size_label.pack(pady=(5, 0))

        # Content cards
        self.content_frame = ttk.Frame(
            self.scrollable_frame
        )
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.cards = []

        for i in range(6):

            card = ttk.LabelFrame(
                self.content_frame,
                text=f"Card {i + 1}",
                padding=15
            )

            label = ttk.Label(
                card,
                text=f"Content untuk card {i + 1}",
                style="Desktop.TLabel"
            )
            label.pack()

            button = ttk.Button(
                card,
                text=f"Action {i + 1}",
                style="Desktop.TButton"
            )
            button.pack(pady=(10, 0))

            self.cards.append(card)

        # Control panel
        self.control_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="Controls",
            padding=15
        )
        self.control_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        ttk.Button(
            self.control_frame,
            text="Simulate Mobile (400x600)",
            command=lambda: self.resize_window(400, 600)
        ).pack(
            side="left",
            padx=(0, 5),
            pady=5
        )

        ttk.Button(
            self.control_frame,
            text="Simulate Tablet (600x800)",
            command=lambda: self.resize_window(600, 800)
        ).pack(
            side="left",
            padx=5,
            pady=5
        )

        ttk.Button(
            self.control_frame,
            text="Simulate Desktop (800x600)",
            command=lambda: self.resize_window(800, 600)
        ).pack(
            side="left",
            padx=5,
            pady=5
        )

        self.update_layout()

    def on_canvas_resize(self, event):

        # Lebar scrollable frame mengikuti canvas
        self.canvas.itemconfigure(
            self.window_id,
            width=event.width
        )

    def on_frame_resize(self, event):

        # Hindari event dari child widget
        if event.widget != self:
            return

        width = self.winfo_width()
        height = self.winfo_height()

        if width < 100:
            return

        self.current_width = width
        self.current_height = height

        self.size_label.config(
            text=f"Window Size: {width}x{height}"
        )

        self.update_layout()

    def update_layout(self):

        width = self.current_width

        # Tentukan jumlah kolom
        if width < 500:
            columns = 1
            size = "Mobile"

        elif width < 700:
            columns = 2
            size = "Tablet"

        else:
            columns = 3
            size = "Desktop"

        # Bersihkan layout lama
        for card in self.cards:
            card.grid_forget()

        # Atur kolom agar proporsional
        for col in range(3):
            self.content_frame.columnconfigure(
                col,
                weight=1 if col < columns else 0
            )

        # Susun card menggunakan grid
        for i, card in enumerate(self.cards):

            row = i // columns
            col = i % columns

            card.grid(
                row=row,
                column=col,
                sticky="nsew",
                padx=5,
                pady=5
            )

        self.update_styles(size)

    def update_styles(self, size):

        label_style = f"{size}.TLabel"
        button_style = f"{size}.TButton"

        self.title_label.configure(
            style=label_style
        )

        self.size_label.configure(
            style=label_style
        )

        for card in self.cards:

            for child in card.winfo_children():

                if isinstance(child, ttk.Label):
                    child.configure(style=label_style)

                elif isinstance(child, ttk.Button):
                    child.configure(style=button_style)

    def resize_window(self, width, height):

        root = self.winfo_toplevel()
        root.geometry(f"{width}x{height}")

    def run(self):
        pass



class MainApp:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(
            "Praktikum Tkinter - Custom Style & Responsive"
        )

        self.root.geometry("850x650")
        self.root.minsize(400, 400)

        # Theme
        self.style = ttk.Style()

        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self.style.configure(
            "Main.TFrame",
            background="#2c3e50"
        )

        # Notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Tab Custom Styling
        custom_tab = CustomStyleApp(
            notebook,
            self.style
        )

        notebook.add(
            custom_tab,
            text="Custom Styling"
        )

        # Tab Responsive Design
        responsive_tab = ResponsiveApp(
            notebook,
            self.style
        )

        notebook.add(
            responsive_tab,
            text="Responsive Design"
        )

    def run(self):
        self.root.mainloop()



if __name__ == "__main__":

    app = MainApp()
    app.run()
