import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime


class FileExplorer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("File Explorer - File Management Demo")
        self.window.geometry("1000x650")
        self.window.minsize(800, 500)
        self.window.configure(bg="lightsteelblue")

        self.current_file = None
        self.current_directory = os.getcwd()

        self.buat_interface()
        self.show_directory_contents(self.current_directory)

    def buat_interface(self):
        # Header
        header_frame = tk.Frame(self.window, bg="darkblue", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="FILE EXPLORER",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="darkblue"
        ).pack(pady=15)

        # Navigation bar
        nav_frame = tk.Frame(self.window, bg="lightgray", height=42)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        tk.Label(
            nav_frame,
            text="Current Directory:",
            font=("Arial", 10, "bold"),
            bg="lightgray"
        ).pack(side=tk.LEFT, padx=(10, 6), pady=10)

        self.path_label = tk.Label(
            nav_frame,
            text=self.current_directory,
            font=("Arial", 9),
            bg="lightgray",
            fg="blue",
            anchor="w"
        )
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=10)

        # Toolbar
        toolbar = tk.Frame(
            self.window, bg="lightgray", relief=tk.RAISED, bd=1
        )
        toolbar.pack(fill=tk.X, padx=2, pady=2)

        buttons = [
            ("📁 Open File", self.open_file, "lightblue", 12),
            ("📂 Open Directory", self.open_directory, "lightgreen", 15),
            ("📄 Create File", self.create_file, "lightyellow", 12),
            ("🗑 Delete", self.delete_file, "lightcoral", 10),
            ("🔄 Refresh", self.refresh_view, "lightcyan", 10),
        ]

        for text, command, color, width in buttons:
            tk.Button(
                toolbar,
                text=text,
                command=command,
                font=("Arial", 10),
                bg=color,
                width=width,
                cursor="hand2"
            ).pack(side=tk.LEFT, padx=3, pady=4)

        # Main content
        content_frame = tk.Frame(self.window, bg="lightsteelblue")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Panel kiri: informasi file
        left_frame = tk.LabelFrame(
            content_frame,
            text="File Information / Directory Contents",
            font=("Arial", 11, "bold"),
            bg="lightsteelblue"
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))

        self.info_text = tk.Text(
            left_frame,
            font=("Consolas", 9),
            bg="white",
            wrap=tk.WORD,
            height=15,
            state=tk.NORMAL
        )
        info_scrollbar = tk.Scrollbar(
            left_frame, orient=tk.VERTICAL, command=self.info_text.yview
        )
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        self.info_text.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5
        )
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)

        # Panel kanan: preview
        right_frame = tk.LabelFrame(
            content_frame,
            text="File Preview",
            font=("Arial", 11, "bold"),
            bg="lightsteelblue"
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))

        self.preview_text = tk.Text(
            right_frame,
            font=("Consolas", 9),
            bg="lightyellow",
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED
        )
        preview_scrollbar = tk.Scrollbar(
            right_frame, orient=tk.VERTICAL, command=self.preview_text.yview
        )
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)
        self.preview_text.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5
        )
        preview_scrollbar.pack(
            side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5
        )

        # Status bar
        self.status_label = tk.Label(
            self.window,
            text="Ready",
            anchor="w",
            bg="darkblue",
            fg="white",
            padx=8,
            pady=4
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def set_info(self, content):
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", content)

    def set_preview(self, content):
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", content)
        self.preview_text.config(state=tk.DISABLED)

    def update_directory_info(self):
        self.path_label.config(text=self.current_directory)

    def set_status(self, message):
        self.status_label.config(text=message)

    def format_file_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        if size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.1f} KB"
        if size_bytes < 1024 ** 3:
            return f"{size_bytes / (1024 ** 2):.1f} MB"
        return f"{size_bytes / (1024 ** 3):.1f} GB"

    def get_file_type(self, filepath):
        extension = os.path.splitext(filepath)[1].lower()
        file_types = {
            ".txt": "Text Document",
            ".py": "Python Script",
            ".json": "JSON Data",
            ".csv": "CSV Data",
            ".html": "HTML Document",
            ".css": "CSS Stylesheet",
            ".js": "JavaScript",
            ".jpg": "JPEG Image",
            ".jpeg": "JPEG Image",
            ".png": "PNG Image",
            ".gif": "GIF Image",
            ".pdf": "PDF Document",
            ".docx": "Word Document",
            ".xlsx": "Excel Spreadsheet",
            ".md": "Markdown Document",
            ".xml": "XML Document",
            ".log": "Log File",
        }
        return file_types.get(extension, "Unknown File Type")

    def open_file(self):
        file_types = [
            ("Text files", "*.txt"),
            ("Python files", "*.py"),
            ("JSON files", "*.json"),
            ("CSV files", "*.csv"),
            ("All files", "*.*"),
        ]

        filename = filedialog.askopenfilename(
            title="Select a file to open",
            filetypes=file_types,
            initialdir=self.current_directory
        )
        if not filename:
            return

        try:
            self.current_file = os.path.abspath(filename)
            self.current_directory = os.path.dirname(self.current_file)
            self.update_directory_info()
            self.show_file_info(self.current_file)
            self.preview_file(self.current_file)
            self.set_status(f"Opened: {os.path.basename(self.current_file)}")
        except OSError as exc:
            messagebox.showerror("Error", f"Cannot open file:\n{exc}")

    def show_file_info(self, filepath):
        try:
            stat_info = os.stat(filepath)
            modified_time = datetime.fromtimestamp(stat_info.st_mtime)
            created_time = datetime.fromtimestamp(stat_info.st_ctime)

            info = f"""FILE INFORMATION
{'=' * 42}

File Name : {os.path.basename(filepath)}
Full Path : {filepath}
Directory : {os.path.dirname(filepath)}

File Size : {self.format_file_size(stat_info.st_size)}
Extension : {os.path.splitext(filepath)[1] or 'No extension'}
File Type : {self.get_file_type(filepath)}

Created  : {created_time:%Y-%m-%d %H:%M:%S}
Modified : {modified_time:%Y-%m-%d %H:%M:%S}

Permissions:
- Readable   : {'Yes' if os.access(filepath, os.R_OK) else 'No'}
- Writable   : {'Yes' if os.access(filepath, os.W_OK) else 'No'}
- Executable : {'Yes' if os.access(filepath, os.X_OK) else 'No'}
"""
            self.set_info(info)
        except OSError as exc:
            self.set_info(f"Error getting file information:\n{exc}")

    def preview_file(self, filepath):
        try:
            file_size = os.path.getsize(filepath)

            if file_size > 1024 * 1024:
                preview_content = (
                    f"File too large for preview "
                    f"({self.format_file_size(file_size)}).\n\n"
                    "Preview is limited to files up to 1 MB."
                )
            else:
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        content = file.read(5001)

                    if len(content) > 5000:
                        preview_content = (
                            content[:5000] +
                            "\n\n... (Content truncated for preview)"
                        )
                    else:
                        preview_content = content or "(File is empty)"
                except UnicodeDecodeError:
                    with open(filepath, "rb") as file:
                        binary_content = file.read(500)

                    hex_content = " ".join(f"{byte:02x}" for byte in binary_content)
                    preview_content = (
                        "Binary file detected.\n"
                        "Showing the first 500 bytes as hexadecimal:\n\n"
                        f"{hex_content}"
                    )

            self.set_preview(preview_content)
        except OSError as exc:
            self.set_preview(f"Error previewing file:\n{exc}")

    def open_directory(self):
        directory = filedialog.askdirectory(
            title="Select a directory",
            initialdir=self.current_directory
        )
        if not directory:
            return

        self.current_directory = os.path.abspath(directory)
        self.current_file = None
        self.update_directory_info()
        self.show_directory_contents(self.current_directory)
        self.set_status(f"Directory opened: {self.current_directory}")

    def show_directory_contents(self, directory):
        try:
            items = os.listdir(directory)
            folders, files = [], []

            for item in items:
                item_path = os.path.join(directory, item)
                try:
                    if os.path.isdir(item_path):
                        folders.append(item)
                    else:
                        files.append(item)
                except OSError:
                    files.append(item)

            folders.sort(key=str.lower)
            files.sort(key=str.lower)

            lines = [
                "DIRECTORY CONTENTS",
                "=" * 42,
                "",
                f"Directory   : {directory}",
                f"Total items : {len(items)}",
                f"Folders     : {len(folders)}",
                f"Files       : {len(files)}",
                "",
                f"FOLDERS ({len(folders)})",
                "-" * 30,
            ]

            for folder in folders:
                folder_path = os.path.join(directory, folder)
                try:
                    size = self.get_directory_size(folder_path)
                    lines.append(
                        f"[DIR]  {folder} ({self.format_file_size(size)})"
                    )
                except OSError:
                    lines.append(f"[DIR]  {folder} (Size unknown)")

            lines.extend(["", f"FILES ({len(files)})", "-" * 30])

            for filename in files:
                file_path = os.path.join(directory, filename)
                try:
                    size = os.path.getsize(file_path)
                    extension = os.path.splitext(filename)[1]
                    lines.append(
                        f"[FILE] {filename} "
                        f"({self.format_file_size(size)}) {extension}"
                    )
                except OSError:
                    lines.append(f"[FILE] {filename} (Size unknown)")

            self.set_info("\n".join(lines))
            self.set_preview(
                "Pilih tombol Open File untuk melihat isi file.\n\n"
                "Informasi folder dan daftar isinya ditampilkan di panel kiri."
            )
            self.set_status(f"{len(folders)} folder, {len(files)} file")
        except OSError as exc:
            self.set_info(f"Error reading directory:\n{exc}")
            messagebox.showerror("Error", f"Cannot read directory:\n{exc}")

    def get_directory_size(self, directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory, onerror=lambda e: None):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except OSError:
                    continue
        return total_size

    def create_file(self):
        filename = filedialog.asksaveasfilename(
            title="Create new file",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JSON files", "*.json"),
                ("All files", "*.*"),
            ],
            initialdir=self.current_directory
        )
        if not filename:
            return

        # Hindari mengosongkan file yang sudah ada tanpa konfirmasi.
        if os.path.exists(filename):
            overwrite = messagebox.askyesno(
                "File already exists",
                "File tersebut sudah ada. Kosongkan isinya?"
            )
            if not overwrite:
                return

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write("")

            self.current_file = os.path.abspath(filename)
            self.current_directory = os.path.dirname(self.current_file)
            self.update_directory_info()
            self.show_file_info(self.current_file)
            self.set_preview("New empty file created.")
            self.set_status(f"Created: {os.path.basename(self.current_file)}")
            messagebox.showinfo(
                "Success",
                f"File created:\n{os.path.basename(self.current_file)}"
            )
        except OSError as exc:
            messagebox.showerror("Error", f"Cannot create file:\n{exc}")

    def delete_file(self):
        if not self.current_file:
            messagebox.showwarning(
                "Warning",
                "Buka file terlebih dahulu sebelum menghapusnya."
            )
            return

        if not os.path.isfile(self.current_file):
            messagebox.showwarning(
                "Warning",
                "File yang dipilih tidak ditemukan atau bukan file biasa."
            )
            self.current_file = None
            return

        filename = os.path.basename(self.current_file)
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Yakin ingin menghapus '{filename}'?\n\n"
            "Tindakan ini tidak dapat dibatalkan."
        )
        if not confirm:
            return

        try:
            os.remove(self.current_file)
            deleted_name = filename
            self.current_file = None
            self.set_info(f"File '{deleted_name}' berhasil dihapus.")
            self.set_preview("No file selected.")
            self.show_directory_contents(self.current_directory)
            self.set_status(f"Deleted: {deleted_name}")
            messagebox.showinfo(
                "Success", f"File '{deleted_name}' berhasil dihapus."
            )
        except OSError as exc:
            messagebox.showerror("Error", f"Cannot delete file:\n{exc}")

    def refresh_view(self):
        if self.current_file and os.path.isfile(self.current_file):
            self.show_file_info(self.current_file)
            self.preview_file(self.current_file)
            self.set_status("File view refreshed.")
        elif os.path.isdir(self.current_directory):
            self.current_file = None
            self.update_directory_info()
            self.show_directory_contents(self.current_directory)
            self.set_status("Directory view refreshed.")
        else:
            self.current_file = None
            self.current_directory = os.path.expanduser("~")
            self.update_directory_info()
            self.show_directory_contents(self.current_directory)

    def jalankan(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = FileExplorer()
    app.jalankan()
