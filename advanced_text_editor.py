import os
import re
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, scrolledtext, ttk, font


class AdvancedTextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Advanced Text Editor - Untitled")
        self.window.geometry("1000x720")
        self.window.minsize(700, 450)
        self.window.configure(bg="white")

        # File state
        self.current_file = None
        self.is_modified = False
        self.recent_files = []
        self.max_recent_files = 10
        self._loading_file = False
        self._status_after_id = None

        # View state
        self.current_font = ("Consolas", 12)
        self.word_wrap = True
        self.show_line_numbers = True

        self.buat_interface()
        self.buat_menu_system()
        self.bind_events()
        self.update_title()
        self.update_cursor_position()
        self.text_area.focus_set()

    def buat_interface(self):
        self.toolbar = tk.Frame(self.window, bg="lightgray", relief=tk.RAISED, bd=1)
        self.toolbar.pack(fill=tk.X)
        self.buat_toolbar_buttons()

        editor_frame = tk.Frame(self.window, bg="white")
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.line_numbers_frame = tk.Frame(editor_frame, bg="#eeeeee", width=48)
        self.line_numbers = tk.Text(
            self.line_numbers_frame, width=5, padx=5, takefocus=0,
            borderwidth=0, background="#eeeeee", foreground="#666666",
            state="disabled", font=self.current_font, wrap=tk.NONE
        )
        self.line_numbers.pack(fill=tk.Y, expand=True)
        self.line_numbers_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.text_area = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD if self.word_wrap else tk.NONE,
            undo=True, maxundo=-1, autoseparators=True,
            font=self.current_font, bg="white", fg="black",
            insertbackground="black", selectbackground="lightblue",
            padx=8, pady=8, relief=tk.FLAT
        )
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.status_bar = tk.Frame(self.window, relief=tk.SUNKEN, bd=1, bg="#f4f4f4")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = tk.Label(self.status_bar, text="Ready", anchor=tk.W,
                                     font=("Arial", 9), bg="#f4f4f4")
        self.status_label.pack(side=tk.LEFT, padx=5)
        self.position_label = tk.Label(self.status_bar, text="Line: 1, Column: 1",
                                       anchor=tk.E, font=("Arial", 9), bg="#f4f4f4")
        self.position_label.pack(side=tk.RIGHT, padx=5)
        self.file_info_label = tk.Label(self.status_bar, text="Untitled", anchor=tk.CENTER,
                                        font=("Arial", 9), bg="#f4f4f4")
        self.file_info_label.pack(side=tk.RIGHT, padx=20)

        self.update_line_numbers()

    def buat_toolbar_buttons(self):
        buttons = [
            ("📄 New", self.new_file), ("📁 Open", self.open_file),
            ("💾 Save", self.save_file), ("↶ Undo", self.undo_action),
            ("↷ Redo", self.redo_action), ("🔍 Find", self.show_find_dialog),
            ("🔤 Font", self.change_font),
        ]
        for index, (label, command) in enumerate(buttons):
            if index in (3, 5):
                tk.Frame(self.toolbar, width=2, bg="gray", relief=tk.SUNKEN, bd=1).pack(
                    side=tk.LEFT, fill=tk.Y, padx=5, pady=2
                )
            tk.Button(self.toolbar, text=label, command=command, relief=tk.FLAT,
                      bg="lightgray", font=("Arial", 9), padx=5).pack(
                side=tk.LEFT, padx=2, pady=2
            )

    def buat_menu_system(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Recent Files", menu=self.recent_menu)
        self.update_recent_menu()
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo_action, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo_action, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Find...", command=self.show_find_dialog, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace...", command=self.show_replace_dialog, accelerator="Ctrl+H")

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        self.wrap_var = tk.BooleanVar(value=self.word_wrap)
        view_menu.add_checkbutton(label="Word Wrap", variable=self.wrap_var, command=self.toggle_word_wrap)
        self.line_numbers_var = tk.BooleanVar(value=self.show_line_numbers)
        view_menu.add_checkbutton(label="Show Line Numbers", variable=self.line_numbers_var,
                                  command=self.toggle_line_numbers)
        view_menu.add_separator()
        view_menu.add_command(label="Change Font...", command=self.change_font)

        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Word Count", command=self.show_word_count)
        tools_menu.add_command(label="Character Count", command=self.show_char_count)
        tools_menu.add_separator()
        tools_menu.add_command(label="Insert Date/Time", command=self.insert_datetime)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def bind_events(self):
        shortcuts = {
            "<Control-n>": self.new_file,
            "<Control-o>": self.open_file,
            "<Control-s>": self.save_file,
            "<Control-Shift-S>": self.save_as_file,
            "<Control-q>": self.on_closing,
            "<Control-z>": self.undo_action,
            "<Control-y>": self.redo_action,
            "<Control-x>": self.cut_text,
            "<Control-c>": self.copy_text,
            "<Control-v>": self.paste_text,
            "<Control-a>": self.select_all,
            "<Control-f>": self.show_find_dialog,
            "<Control-h>": self.show_replace_dialog,
        }
        for sequence, callback in shortcuts.items():
            self.window.bind(sequence, lambda event, cb=callback: (cb(), "break")[1])

        self.text_area.bind("<<Modified>>", self.on_text_change)
        self.text_area.bind("<KeyRelease>", self.on_cursor_move)
        self.text_area.bind("<ButtonRelease-1>", self.on_cursor_move)
        self.text_area.bind("<MouseWheel>", self.on_cursor_move)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    # File operations
    def new_file(self):
        if not self.confirm_save():
            return
        self._loading_file = True
        self.text_area.delete("1.0", tk.END)
        self.text_area.edit_reset()
        self._loading_file = False
        self.current_file = None
        self.is_modified = False
        self.update_title()
        self.update_line_numbers()
        self.update_status("New file created")

    def open_file(self):
        if not self.confirm_save():
            return
        file_types = [("Text files", "*.txt"), ("Python files", "*.py"),
                      ("JavaScript files", "*.js"), ("HTML files", "*.html"),
                      ("CSS files", "*.css"), ("JSON files", "*.json"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Open File", filetypes=file_types)
        if filename:
            self.load_file(filename)

    def load_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            self._loading_file = True
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)
            self.text_area.edit_reset()
            self.text_area.edit_modified(False)
            self._loading_file = False
            self.current_file = filename
            self.is_modified = False
            self.add_to_recent_files(filename)
            self.update_title()
            self.update_line_numbers()
            self.update_status(f"Opened: {os.path.basename(filename)}")
        except (OSError, UnicodeError) as error:
            self._loading_file = False
            messagebox.showerror("Error", f"Cannot open file:\n{error}")

    def save_file(self):
        if not self.current_file:
            return self.save_as_file()
        return self._write_file(self.current_file)

    def save_as_file(self):
        file_types = [("Text files", "*.txt"), ("Python files", "*.py"),
                      ("JavaScript files", "*.js"), ("HTML files", "*.html"),
                      ("CSS files", "*.css"), ("JSON files", "*.json"), ("All files", "*.*")]
        filename = filedialog.asksaveasfilename(title="Save As", filetypes=file_types,
                                                defaultextension=".txt")
        if not filename:
            return False
        return self._write_file(filename)

    def _write_file(self, filename):
        try:
            content = self.text_area.get("1.0", "end-1c")
            with open(filename, "w", encoding="utf-8", newline="") as file:
                file.write(content)
            self.current_file = filename
            self.is_modified = False
            self.text_area.edit_modified(False)
            self.add_to_recent_files(filename)
            self.update_title()
            self.update_status(f"Saved: {os.path.basename(filename)}")
            return True
        except OSError as error:
            messagebox.showerror("Error", f"Cannot save file:\n{error}")
            return False

    def confirm_save(self):
        if not self.is_modified:
            return True
        response = messagebox.askyesnocancel(
            "Save Changes", "Do you want to save changes to the current document?"
        )
        if response is True:
            return self.save_file()
        if response is False:
            return True
        return False

    def on_closing(self):
        if self.confirm_save():
            self.window.destroy()

    # Recent files
    def add_to_recent_files(self, filename):
        filename = os.path.abspath(filename)
        if filename in self.recent_files:
            self.recent_files.remove(filename)
        self.recent_files.insert(0, filename)
        self.recent_files = self.recent_files[:self.max_recent_files]
        self.update_recent_menu()

    def update_recent_menu(self):
        if not hasattr(self, "recent_menu"):
            return
        self.recent_menu.delete(0, tk.END)
        if not self.recent_files:
            self.recent_menu.add_command(label="No recent files", state=tk.DISABLED)
            return
        for index, filename in enumerate(self.recent_files):
            display_name = os.path.basename(filename)
            if len(display_name) > 30:
                display_name = display_name[:27] + "..."
            self.recent_menu.add_command(label=f"{index + 1}. {display_name}",
                                         command=lambda path=filename: self.open_recent_file(path))
        self.recent_menu.add_separator()
        self.recent_menu.add_command(label="Clear Recent Files", command=self.clear_recent_files)

    def open_recent_file(self, filename):
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"File not found:\n{filename}")
            if filename in self.recent_files:
                self.recent_files.remove(filename)
            self.update_recent_menu()
            return
        if self.confirm_save():
            self.load_file(filename)

    def clear_recent_files(self):
        if messagebox.askyesno("Clear Recent Files", "Clear all recent files from the list?"):
            self.recent_files.clear()
            self.update_recent_menu()

    # Edit operations
    def undo_action(self):
        try:
            self.text_area.edit_undo()
            self.update_status("Undo performed")
        except tk.TclError:
            self.update_status("Nothing to undo")

    def redo_action(self):
        try:
            self.text_area.edit_redo()
            self.update_status("Redo performed")
        except tk.TclError:
            self.update_status("Nothing to redo")

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")
        self.update_status("Text cut to clipboard")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")
        self.update_status("Text copied to clipboard")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")
        self.update_status("Text pasted from clipboard")

    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", "end-1c")
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        self.update_status("All text selected")

    # Find and replace
    def show_find_dialog(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Find")
        dialog.geometry("420x170")
        dialog.transient(self.window)
        dialog.resizable(False, False)
        dialog.grab_set()
        tk.Label(dialog, text="Find:").pack(pady=(10, 2))
        self.find_entry = tk.Entry(dialog, width=45)
        self.find_entry.pack(pady=3)
        self.find_entry.focus_set()
        options = tk.Frame(dialog)
        options.pack(pady=3)
        self.case_sensitive_var = tk.BooleanVar(value=False)
        self.whole_word_var = tk.BooleanVar(value=False)
        tk.Checkbutton(options, text="Case sensitive", variable=self.case_sensitive_var).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(options, text="Whole word", variable=self.whole_word_var).pack(side=tk.LEFT, padx=5)
        buttons = tk.Frame(dialog)
        buttons.pack(pady=8)
        tk.Button(buttons, text="Find Next", command=self.find_next, width=10).pack(side=tk.LEFT, padx=4)
        tk.Button(buttons, text="Find All", command=self.find_all, width=10).pack(side=tk.LEFT, padx=4)
        tk.Button(buttons, text="Close", command=dialog.destroy, width=10).pack(side=tk.LEFT, padx=4)
        self.find_entry.bind("<Return>", lambda event: self.find_next())

    def _search_options(self):
        case_sensitive = getattr(self, "case_sensitive_var", None)
        whole_word = getattr(self, "whole_word_var", None)
        return (case_sensitive.get() if case_sensitive else False,
                whole_word.get() if whole_word else False)

    def _find_positions(self, search_text, start="1.0"):
        case_sensitive, whole_word = self._search_options()
        content = self.text_area.get("1.0", "end-1c")
        start_offset = int(self.text_area.count("1.0", start, "chars")[0] or 0)
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern_text = re.escape(search_text)
        if whole_word:
            pattern_text = r"\b" + pattern_text + r"\b"
        return [(match.start(), match.end()) for match in re.finditer(pattern_text, content, flags) if match.start() >= start_offset], content

    def find_next(self):
        search_text = self.find_entry.get()
        if not search_text:
            return
        positions, content = self._find_positions(search_text, self.text_area.index(tk.INSERT))
        if not positions:
            positions, content = self._find_positions(search_text, "1.0")
            positions = [p for p in positions if p[0] < int(self.text_area.count("1.0", self.text_area.index(tk.INSERT), "chars")[0] or 0)]
        if not positions:
            messagebox.showinfo("Find", f"'{search_text}' not found")
            return
        start, end = positions[0]
        start_index = f"1.0 + {start} chars"
        end_index = f"1.0 + {end} chars"
        self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
        self.text_area.tag_add(tk.SEL, start_index, end_index)
        self.text_area.mark_set(tk.INSERT, end_index)
        self.text_area.see(start_index)
        self.update_status(f"Found: {search_text}")

    def find_all(self):
        search_text = self.find_entry.get()
        if not search_text:
            return
        self.text_area.tag_remove("found", "1.0", tk.END)
        positions, _ = self._find_positions(search_text, "1.0")
        for start, end in positions:
            self.text_area.tag_add("found", f"1.0 + {start} chars", f"1.0 + {end} chars")
        self.text_area.tag_config("found", background="yellow", foreground="black")
        if positions:
            self.update_status(f"Found {len(positions)} occurrences of '{search_text}'")
        else:
            messagebox.showinfo("Find All", f"'{search_text}' not found")

    def show_replace_dialog(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Replace")
        dialog.geometry("420x220")
        dialog.transient(self.window)
        dialog.resizable(False, False)
        dialog.grab_set()
        tk.Label(dialog, text="Find:").pack(pady=(8, 2))
        self.replace_find_entry = tk.Entry(dialog, width=45)
        self.replace_find_entry.pack(pady=2)
        tk.Label(dialog, text="Replace with:").pack(pady=(6, 2))
        self.replace_with_entry = tk.Entry(dialog, width=45)
        self.replace_with_entry.pack(pady=2)
        self.replace_find_entry.focus_set()
        self.replace_case_var = tk.BooleanVar(value=False)
        tk.Checkbutton(dialog, text="Case sensitive", variable=self.replace_case_var).pack(pady=3)
        buttons = tk.Frame(dialog)
        buttons.pack(pady=8)
        tk.Button(buttons, text="Replace", command=self.replace_current, width=11).pack(side=tk.LEFT, padx=4)
        tk.Button(buttons, text="Replace All", command=self.replace_all, width=11).pack(side=tk.LEFT, padx=4)
        tk.Button(buttons, text="Close", command=dialog.destroy, width=11).pack(side=tk.LEFT, padx=4)

    def replace_current(self):
        find_text = self.replace_find_entry.get()
        replacement = self.replace_with_entry.get()
        if not find_text:
            return
        try:
            start, end = self.text_area.index(tk.SEL_FIRST), self.text_area.index(tk.SEL_LAST)
            selected = self.text_area.get(start, end)
        except tk.TclError:
            messagebox.showinfo("Replace", "Select a matching occurrence first. You can use Find to select it.")
            return
        matches = selected == find_text if self.replace_case_var.get() else selected.lower() == find_text.lower()
        if matches:
            self.text_area.delete(start, end)
            self.text_area.insert(start, replacement)
            self.update_status(f"Replaced: {find_text} → {replacement}")
        else:
            messagebox.showinfo("Replace", "Selected text does not match the search text.")

    def replace_all(self):
        find_text = self.replace_find_entry.get()
        replacement = self.replace_with_entry.get()
        if not find_text:
            return
        content = self.text_area.get("1.0", "end-1c")
        if self.replace_case_var.get():
            count = content.count(find_text)
            new_content = content.replace(find_text, replacement)
        else:
            pattern = re.compile(re.escape(find_text), re.IGNORECASE)
            new_content, count = pattern.subn(lambda _: replacement, content)
        if count:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", new_content)
            self.update_status(f"Replaced {count} occurrences")
            messagebox.showinfo("Replace All", f"Replaced {count} occurrences of '{find_text}'")
        else:
            messagebox.showinfo("Replace All", f"'{find_text}' not found")

    # View and tools
    def toggle_word_wrap(self):
        self.word_wrap = self.wrap_var.get()
        self.text_area.config(wrap=tk.WORD if self.word_wrap else tk.NONE)
        self.update_status(f"Word wrap {'enabled' if self.word_wrap else 'disabled'}")

    def toggle_line_numbers(self):
        self.show_line_numbers = self.line_numbers_var.get()
        if self.show_line_numbers:
            self.line_numbers_frame.pack(side=tk.LEFT, fill=tk.Y, before=self.text_area)
        else:
            self.line_numbers_frame.pack_forget()
        self.update_status(f"Line numbers {'enabled' if self.show_line_numbers else 'disabled'}")

    def update_line_numbers(self):
        if not hasattr(self, "line_numbers"):
            return
        line_count = int(self.text_area.index("end-1c").split(".")[0])
        numbers = "\n".join(str(number) for number in range(1, line_count + 1))
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert("1.0", numbers or "1")
        self.line_numbers.config(state="disabled")

    def change_font(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Change Font")
        dialog.geometry("320x210")
        dialog.transient(self.window)
        dialog.grab_set()
        tk.Label(dialog, text="Font Family:").pack(pady=(10, 3))
        families = ["Arial", "Times New Roman", "Courier New", "Consolas", "Verdana"]
        font_var = tk.StringVar(value=self.current_font[0])
        ttk.Combobox(dialog, textvariable=font_var, values=families, state="readonly", width=25).pack(pady=3)
        tk.Label(dialog, text="Font Size:").pack(pady=(8, 3))
        size_var = tk.IntVar(value=self.current_font[1])
        tk.Spinbox(dialog, from_=8, to=72, textvariable=size_var, width=8).pack(pady=3)

        def apply_font():
            try:
                size = max(8, min(72, int(size_var.get())))
            except (ValueError, tk.TclError):
                messagebox.showerror("Font", "Font size must be a number between 8 and 72.")
                return
            self.current_font = (font_var.get(), size)
            self.text_area.config(font=self.current_font)
            self.line_numbers.config(font=self.current_font)
            self.update_line_numbers()
            self.update_status(f"Font changed to {self.current_font[0]} {size}")
            dialog.destroy()

        buttons = tk.Frame(dialog)
        buttons.pack(pady=12)
        tk.Button(buttons, text="Apply", command=apply_font).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def show_word_count(self):
        content = self.text_area.get("1.0", "end-1c")
        messagebox.showinfo("Word Count", f"Words: {len(content.split())}\nLines: {len(content.splitlines()) or 1}")

    def show_char_count(self):
        content = self.text_area.get("1.0", "end-1c")
        no_whitespace = len(re.sub(r"\s", "", content))
        messagebox.showinfo("Character Count", f"Characters: {len(content)}\nCharacters (no whitespace): {no_whitespace}")

    def insert_datetime(self):
        self.text_area.insert(tk.INSERT, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.update_status("Date/time inserted")

    def show_about(self):
        messagebox.showinfo("About", "Advanced Text Editor\nVersion 1.0\n\nA feature-rich text editor built with Python Tkinter.\n\nFeatures: File operations, recent files, find/replace, undo/redo, word wrap, line numbers, font customization, word/character count, and date/time insertion.\n\nCreated for educational purposes.")

    # Status and events
    def on_text_change(self, event=None):
        if self.text_area.edit_modified():
            if not self._loading_file:
                self.is_modified = True
                self.update_title()
                self.update_line_numbers()
            self.text_area.edit_modified(False)

    def on_cursor_move(self, event=None):
        self.update_cursor_position()
        self.update_line_numbers()

    def update_cursor_position(self):
        try:
            line, column = self.text_area.index(tk.INSERT).split(".")
            self.position_label.config(text=f"Line: {line}, Column: {int(column) + 1}")
        except (tk.TclError, AttributeError):
            pass

    def update_title(self):
        filename = os.path.basename(self.current_file) if self.current_file else "Untitled"
        self.file_info_label.config(text=filename)
        self.window.title(f"Advanced Text Editor - {filename}{' *' if self.is_modified else ''}")

    def update_status(self, message):
        self.status_label.config(text=message)
        if self._status_after_id is not None:
            try:
                self.window.after_cancel(self._status_after_id)
            except tk.TclError:
                pass
        self._status_after_id = self.window.after(3000, lambda: self.status_label.config(text="Ready"))

    def jalankan(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = AdvancedTextEditor()
    app.jalankan()
