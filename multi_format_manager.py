import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import io
import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.sax.saxutils import escape, quoteattr


class MultiFormatManager:
    """Pengelola file CSV, JSON, XML, dan TXT."""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Multi-Format File Manager")
        self.window.geometry("1000x700")
        self.window.minsize(760, 500)

        self.current_file = None
        self.current_format = None
        self.data = None
        self.supported_formats = {
            ".csv": "CSV", ".json": "JSON", ".xml": "XML", ".txt": "Text"
        }

        self.buat_interface()

    def buat_interface(self):
        header = tk.Frame(self.window, bg="darkblue", height=58)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header, text="MULTI-FORMAT FILE MANAGER",
            font=("Arial", 16, "bold"), fg="white", bg="darkblue"
        ).pack(pady=15)

        toolbar = tk.Frame(self.window, bg="lightgray", relief=tk.RAISED, bd=1)
        toolbar.pack(fill=tk.X, padx=2, pady=2)
        buttons = [
            ("📁 Load File", self.load_file, "lightblue"),
            ("💾 Save File", self.save_file, "lightgreen"),
            ("🔄 Convert", self.show_convert_dialog, "lightyellow"),
            ("✓ Validate", self.validate_file, "lightcoral"),
        ]
        for label, command, color in buttons:
            tk.Button(
                toolbar, text=label, command=command, bg=color,
                font=("Arial", 10), width=12
            ).pack(side=tk.LEFT, padx=3, pady=4)

        self.file_info_label = tk.Label(
            toolbar, text="No file loaded", font=("Arial", 10), bg="lightgray"
        )
        self.file_info_label.pack(side=tk.RIGHT, padx=10)

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.raw_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.raw_frame, text="Raw Data")
        self.raw_text = tk.Text(self.raw_frame, font=("Consolas", 10), wrap=tk.NONE, undo=True)
        raw_y = ttk.Scrollbar(self.raw_frame, orient=tk.VERTICAL, command=self.raw_text.yview)
        raw_x = ttk.Scrollbar(self.raw_frame, orient=tk.HORIZONTAL, command=self.raw_text.xview)
        self.raw_text.configure(yscrollcommand=raw_y.set, xscrollcommand=raw_x.set)
        self.raw_text.grid(row=0, column=0, sticky="nsew")
        raw_y.grid(row=0, column=1, sticky="ns")
        raw_x.grid(row=1, column=0, sticky="ew")
        self.raw_frame.rowconfigure(0, weight=1)
        self.raw_frame.columnconfigure(0, weight=1)

        self.structured_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.structured_frame, text="Structured View")
        self.tree = ttk.Treeview(self.structured_frame)
        tree_y = ttk.Scrollbar(self.structured_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_x = ttk.Scrollbar(self.structured_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_y.set, xscrollcommand=tree_x.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_y.grid(row=0, column=1, sticky="ns")
        tree_x.grid(row=1, column=0, sticky="ew")
        self.structured_frame.rowconfigure(0, weight=1)
        self.structured_frame.columnconfigure(0, weight=1)

        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Statistics")
        self.stats_text = tk.Text(self.stats_frame, font=("Consolas", 10), wrap=tk.WORD, state=tk.DISABLED)
        stats_y = ttk.Scrollbar(self.stats_frame, orient=tk.VERTICAL, command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_y.set)
        self.stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stats_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.window, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)

    def set_status(self, message):
        self.status_var.set(message)

    def detect_format(self, filename):
        _, ext = os.path.splitext(filename.lower())
        return self.supported_formats.get(ext, "Unknown")

    def load_file(self):
        filename = filedialog.askopenfilename(
            title="Select file to load",
            filetypes=[
                ("Supported files", "*.csv *.json *.xml *.txt"),
                ("CSV files", "*.csv"), ("JSON files", "*.json"),
                ("XML files", "*.xml"), ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if not filename:
            return
        try:
            fmt = self.detect_format(filename)
            if fmt == "Unknown":
                raise ValueError("Format tidak didukung. Pilih file CSV, JSON, XML, atau TXT.")
            with open(filename, "r", encoding="utf-8-sig", newline="") as file:
                raw = file.read()
            parsed = self.parse_content(fmt, raw)
            self.current_file = filename
            self.current_format = fmt
            self.data = parsed
            self.update_file_info()
            self.update_all_views()
            self.set_status(f"Loaded: {os.path.basename(filename)}")
            messagebox.showinfo("Success", f"File loaded: {os.path.basename(filename)}")
        except Exception as exc:
            messagebox.showerror("Load Error", f"Tidak dapat membuka file:\n{exc}")

    def parse_content(self, fmt, raw):
        if fmt == "CSV":
            rows = list(csv.reader(io.StringIO(raw)))
            headers = rows[0] if rows else []
            return {"type": "csv", "headers": headers, "rows": rows[1:] if rows else [], "raw_content": raw}
        if fmt == "JSON":
            return {"type": "json", "content": json.loads(raw), "raw_content": raw}
        if fmt == "XML":
            root = ET.fromstring(raw)
            return {"type": "xml", "root": root, "raw_content": raw}
        return {"type": "text", "content": raw, "raw_content": raw}

    def update_file_info(self):
        if self.current_file:
            self.file_info_label.config(
                text=f"{os.path.basename(self.current_file)} ({self.current_format})"
            )
        else:
            self.file_info_label.config(text="No file loaded")

    def update_all_views(self):
        self.update_raw_view()
        self.update_structured_view()
        self.update_statistics()

    def update_raw_view(self):
        raw = self.data.get("raw_content", "") if self.data else ""
        self.raw_text.delete("1.0", tk.END)
        self.raw_text.insert("1.0", raw)

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()
        self.tree["show"] = "tree"

    def update_structured_view(self):
        self.clear_tree()
        if not self.data:
            return
        kind = self.data["type"]
        if kind == "csv":
            headers = self.data["headers"]
            rows = self.data["rows"]
            if headers:
                # Treeview column identifiers must be unique.
                columns = [f"col{i}" for i in range(len(headers))]
                self.tree["columns"] = columns
                self.tree["show"] = "headings"
                for i, col in enumerate(columns):
                    self.tree.heading(col, text=headers[i] or f"Column {i + 1}")
                    self.tree.column(col, width=130, minwidth=70)
                for row in rows:
                    padded = row + [""] * max(0, len(headers) - len(row))
                    self.tree.insert("", tk.END, values=padded[:len(headers)])
            else:
                self.tree["columns"] = ("data",)
                self.tree["show"] = "headings"
                self.tree.heading("data", text="Data")
                for row in rows:
                    self.tree.insert("", tk.END, values=(str(row),))
        elif kind == "json":
            self.tree["columns"] = ("value",)
            self.tree["show"] = "tree headings"
            self.tree.heading("#0", text="Key / Index")
            self.tree.heading("value", text="Value")
            self._add_json_node("", "Root", self.data["content"])
        elif kind == "xml":
            self.tree["columns"] = ("attributes", "text")
            self.tree["show"] = "tree headings"
            self.tree.heading("#0", text="Element")
            self.tree.heading("attributes", text="Attributes")
            self.tree.heading("text", text="Text Content")
            self._add_xml_node("", self.data["root"])
        else:
            self.tree["columns"] = ("content",)
            self.tree["show"] = "tree headings"
            self.tree.heading("#0", text="Line")
            self.tree.heading("content", text="Content")
            for i, line in enumerate(self.data["content"].splitlines() or [""], 1):
                self.tree.insert("", tk.END, text=f"Line {i}", values=(line,))

    def _add_json_node(self, parent, key, value):
        if isinstance(value, dict):
            node = self.tree.insert(parent, tk.END, text=str(key), values=(f"Object ({len(value)} keys)",))
            for k, v in value.items():
                self._add_json_node(node, k, v)
        elif isinstance(value, list):
            node = self.tree.insert(parent, tk.END, text=str(key), values=(f"Array ({len(value)} items)",))
            for i, item in enumerate(value):
                self._add_json_node(node, f"[{i}]", item)
        else:
            self.tree.insert(parent, tk.END, text=str(key), values=(repr(value),))

    def _add_xml_node(self, parent, element):
        attrs = ", ".join(f"{k}={v}" for k, v in element.attrib.items())
        node = self.tree.insert(
            parent, tk.END, text=element.tag,
            values=(attrs, (element.text or "").strip())
        )
        for child in element:
            self._add_xml_node(node, child)

    def update_statistics(self):
        if not self.data:
            stats = "No data loaded."
        elif self.data["type"] == "csv":
            stats = self.csv_statistics()
        elif self.data["type"] == "json":
            stats = self.json_statistics()
        elif self.data["type"] == "xml":
            stats = self.xml_statistics()
        else:
            stats = self.text_statistics()
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", stats)
        self.stats_text.config(state=tk.DISABLED)

    def csv_statistics(self):
        headers, rows = self.data["headers"], self.data["rows"]
        lines = [
            "CSV FILE STATISTICS", "=" * 48,
            f"File: {os.path.basename(self.current_file) if self.current_file else 'Unsaved'}",
            f"Headers: {len(headers)}", f"Data rows: {len(rows)}",
            f"Total rows including header: {len(rows) + bool(headers)}", "", "HEADERS:"
        ]
        lines.extend(f"{i}. {h}" for i, h in enumerate(headers, 1))
        for i, header in enumerate(headers):
            values = [r[i].strip() for r in rows if i < len(r) and r[i].strip()]
            lines.extend(["", f"Column '{header}':", f"  Non-empty values: {len(values)}",
                          f"  Empty values: {len(rows) - len(values)}"])
            numeric = []
            for value in values:
                try:
                    numeric.append(float(value))
                except ValueError:
                    pass
            if numeric:
                lines.extend([f"  Numeric values: {len(numeric)}", f"  Min: {min(numeric):g}",
                              f"  Max: {max(numeric):g}", f"  Average: {sum(numeric)/len(numeric):.2f}"])
            elif values:
                lines.append(f"  Unique values: {len(set(values))}")
        return "\n".join(lines)

    def json_statistics(self):
        counts = {}
        def walk(obj, depth=0):
            typ = type(obj).__name__
            counts[typ] = counts.get(typ, 0) + 1
            indent = "  " * depth
            if isinstance(obj, dict):
                result = f"{indent}Object ({len(obj)} keys)\n"
                for k, v in obj.items():
                    result += f"{indent}  {k}: " + walk(v, depth + 1)
                return result
            if isinstance(obj, list):
                result = f"{indent}Array ({len(obj)} items)\n"
                for i, v in enumerate(obj[:3]):
                    result += f"{indent}  [{i}]: " + walk(v, depth + 1)
                if len(obj) > 3:
                    result += f"{indent}  ... {len(obj)-3} more items\n"
                return result
            value = repr(obj)
            return f"{typ} = {value[:80]}\n"
        structure = walk(self.data["content"])
        return (f"JSON FILE STATISTICS\n{'='*48}\n"
                f"File: {os.path.basename(self.current_file) if self.current_file else 'Unsaved'}\n\n"
                f"STRUCTURE:\n{structure}\nTYPE DISTRIBUTION:\n" +
                "\n".join(f"- {k}: {v}" for k, v in sorted(counts.items())))

    def xml_statistics(self):
        counts, attrs = {}, {}
        total = 0
        text_count = 0
        def walk(element):
            nonlocal total, text_count
            total += 1
            counts[element.tag] = counts.get(element.tag, 0) + 1
            if (element.text or "").strip():
                text_count += 1
            for attr in element.attrib:
                attrs[attr] = attrs.get(attr, 0) + 1
            for child in element:
                walk(child)
        root = self.data["root"]
        walk(root)
        lines = [
            "XML FILE STATISTICS", "=" * 48,
            f"File: {os.path.basename(self.current_file) if self.current_file else 'Unsaved'}",
            f"Root element: {root.tag}", f"Total elements: {total}",
            f"Elements with text: {text_count}", f"Unique element types: {len(counts)}",
            f"Unique attributes: {len(attrs)}", "", "ELEMENT DISTRIBUTION:"
        ]
        lines.extend(f"- {k}: {v}" for k, v in sorted(counts.items(), key=lambda x: -x[1]))
        if attrs:
            lines.extend(["", "ATTRIBUTE DISTRIBUTION:"])
            lines.extend(f"- {k}: {v}" for k, v in sorted(attrs.items(), key=lambda x: -x[1]))
        return "\n".join(lines)

    def text_statistics(self):
        content = self.data["content"]
        words = content.lower().split()
        freq = {}
        for word in words:
            clean = "".join(c for c in word if c.isalnum())
            if clean:
                freq[clean] = freq.get(clean, 0) + 1
        paragraphs = len([p for p in content.split("\\n\\n") if p.strip()])
        lines = [
            "TEXT FILE STATISTICS", "=" * 48,
            f"File: {os.path.basename(self.current_file) if self.current_file else 'Unsaved'}",
            f"Characters: {len(content)}",
            f"Characters (no whitespace): {sum(not c.isspace() for c in content)}",
            f"Words: {len(content.split())}", f"Lines: {len(content.splitlines()) or 1}",
            f"Paragraphs: {paragraphs}",
            "", "CHARACTER ANALYSIS:",
            f"Spaces: {content.count(' ')}", f"Tabs: {content.count(chr(9))}",
            f"Newlines: {content.count(chr(10))}",
            f"Digits: {sum(c.isdigit() for c in content)}",
            f"Letters: {sum(c.isalpha() for c in content)}",
            f"Uppercase: {sum(c.isupper() for c in content)}",
            f"Lowercase: {sum(c.islower() for c in content)}",
            "", "MOST FREQUENT WORDS:"
        ]
        lines.extend(f"- {word}: {count}" for word, count in sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:10])
        return "\n".join(lines)

    def validate_file(self):
        if not self.data:
            messagebox.showwarning("Warning", "No file loaded!")
            return
        kind = self.data["type"]
        if kind == "csv":
            headers, rows = self.data["headers"], self.data["rows"]
            issues = [f"Row {i}: expected {len(headers)} columns, found {len(row)}"
                      for i, row in enumerate(rows, 2) if headers and len(row) != len(headers)]
            empty = sum(not cell.strip() for row in rows for cell in row)
            result = ["CSV Validation Results", "", "✓ CSV parsed successfully",
                      f"Headers: {len(headers)}", f"Data rows: {len(rows)}"]
            result.append("⚠ Column count mismatch:\n" + "\n".join(issues[:10]) if issues
                          else "✓ All data rows match the header column count")
            result.append(f"⚠ Empty cells: {empty}" if empty else "✓ No empty cells detected")
        elif kind == "json":
            obj = self.data["content"]
            issues = []
            def check(value, path="root"):
                if isinstance(value, dict):
                    if "" in value:
                        issues.append(f"Empty key at {path}")
                    for key, child in value.items():
                        if child is None:
                            issues.append(f"Null value at {path}.{key}")
                        else:
                            check(child, f"{path}.{key}")
                elif isinstance(value, list):
                    for i, child in enumerate(value):
                        check(child, f"{path}[{i}]")
            check(obj)
            result = ["JSON Validation Results", "", "✓ Valid JSON syntax",
                      f"Root type: {type(obj).__name__}"]
            result.append("Potential issues:\n" + "\n".join(issues[:10]) if issues
                          else "✓ No common structural issues detected")
        elif kind == "xml":
            root = self.data["root"]
            elements = list(root.iter())
            empty = sum(not (e.text or "").strip() and len(e) == 0 for e in elements)
            with_attrs = sum(bool(e.attrib) for e in elements)
            result = ["XML Validation Results", "", "✓ Well-formed XML",
                      f"Root element: {root.tag}", f"Total elements: {len(elements)}",
                      f"Elements with attributes: {with_attrs}",
                      f"Empty leaf elements: {empty}"]
        else:
            content = self.data["content"]
            long_lines = [i for i, line in enumerate(content.splitlines(), 1) if len(line) > 200]
            result = ["Text Validation Results", "", "✓ File readable as UTF-8",
                      f"Characters: {len(content)}", f"Lines: {len(content.splitlines()) or 1}",
                      "✓ Text can be encoded as UTF-8",
                      f"⚠ Lines longer than 200 characters: {len(long_lines)}" if long_lines
                      else "✓ All lines are at most 200 characters"]
        messagebox.showinfo("Validation Result", "\n".join(result))

    def show_convert_dialog(self):
        if not self.data:
            messagebox.showwarning("Warning", "No file loaded!")
            return
        dialog = tk.Toplevel(self.window)
        dialog.title("Convert File Format")
        dialog.geometry("350x280")
        dialog.transient(self.window)
        dialog.grab_set()
        tk.Label(dialog, text=f"Convert from {self.current_format}",
                 font=("Arial", 14, "bold")).pack(pady=12)
        tk.Label(dialog, text="Select target format:").pack(pady=5)
        target = tk.StringVar(value=next((f for f in ("CSV", "JSON", "XML", "Text")
                                          if f != self.current_format), "JSON"))
        for fmt in ("CSV", "JSON", "XML", "Text"):
            if fmt != self.current_format:
                ttk.Radiobutton(dialog, text=fmt, variable=target, value=fmt).pack(anchor="w", padx=55)
        buttons = tk.Frame(dialog)
        buttons.pack(pady=18)
        tk.Button(buttons, text="Convert", command=lambda: self.perform_conversion(target.get(), dialog),
                  bg="green", fg="white", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons, text="Cancel", command=dialog.destroy, width=10).pack(side=tk.LEFT, padx=5)

    def perform_conversion(self, target_format, dialog):
        try:
            converted = self.convert_content(target_format)
            extension = {"CSV": ".csv", "JSON": ".json", "XML": ".xml", "Text": ".txt"}[target_format]
            filename = filedialog.asksaveasfilename(
                title=f"Save as {target_format}", defaultextension=extension,
                filetypes=[(f"{target_format} files", f"*{extension}"), ("All files", "*.*")]
            )
            if not filename:
                return
            with open(filename, "w", encoding="utf-8", newline="") as file:
                file.write(converted)
            dialog.destroy()
            self.set_status(f"Converted to {os.path.basename(filename)}")
            messagebox.showinfo("Success", f"File converted and saved as {target_format}.")
        except Exception as exc:
            messagebox.showerror("Conversion Error", f"Cannot convert file:\n{exc}")

    def convert_content(self, target):
        kind = self.data["type"]
        if target == "Text":
            return self.data.get("raw_content", "")
        if target == "JSON":
            if kind == "json":
                obj = self.data["content"]
            elif kind == "csv":
                headers = self.data["headers"]
                obj = []
                for row in self.data["rows"]:
                    obj.append({header: (row[i] if i < len(row) else "")
                                for i, header in enumerate(headers)})
            elif kind == "xml":
                def elem_to_obj(el):
                    result = {}
                    if el.attrib:
                        result["@attributes"] = el.attrib
                    children = list(el)
                    text_value = (el.text or "").strip()
                    if children:
                        for child in children:
                            value = elem_to_obj(child)
                            if child.tag in result:
                                if not isinstance(result[child.tag], list):
                                    result[child.tag] = [result[child.tag]]
                                result[child.tag].append(value)
                            else:
                                result[child.tag] = value
                        if text_value:
                            result["#text"] = text_value
                        return result
                    return text_value if not result else {**result, "#text": text_value}
                obj = {self.data["root"].tag: elem_to_obj(self.data["root"])}
            else:
                obj = {"content": self.data["content"]}
            return json.dumps(obj, indent=2, ensure_ascii=False)

        if target == "CSV":
            output = io.StringIO(newline="")
            if kind == "csv":
                return self.data["raw_content"]
            if kind == "json":
                obj = self.data["content"]
                if isinstance(obj, list) and all(isinstance(item, dict) for item in obj):
                    keys = list(dict.fromkeys(k for item in obj for k in item.keys()))
                    writer = csv.DictWriter(output, fieldnames=keys, extrasaction="ignore")
                    if keys:
                        writer.writeheader()
                        writer.writerows(obj)
                elif isinstance(obj, dict):
                    writer = csv.writer(output)
                    writer.writerow(["Key", "Value"])
                    for key, value in obj.items():
                        writer.writerow([key, json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value])
                else:
                    writer = csv.writer(output)
                    writer.writerow(["Value"])
                    writer.writerow([obj])
            elif kind == "xml":
                root = self.data["root"]
                rows = []
                for child in list(root):
                    row = {"tag": child.tag, **{f"@{k}": v for k, v in child.attrib.items()}}
                    if list(child):
                        for grandchild in child:
                            row[grandchild.tag] = (grandchild.text or "").strip()
                    else:
                        row["text"] = (child.text or "").strip()
                    rows.append(row)
                keys = list(dict.fromkeys(k for row in rows for k in row.keys()))
                writer = csv.DictWriter(output, fieldnames=keys, extrasaction="ignore")
                if keys:
                    writer.writeheader()
                    writer.writerows(rows)
            else:
                writer = csv.writer(output)
                writer.writerow(["Line", "Content"])
                writer.writerows([[i, line] for i, line in enumerate(self.data["content"].splitlines(), 1)])
            return output.getvalue()

        if target == "XML":
            if kind == "xml":
                return self.data["raw_content"]
            root = ET.Element("root")
            if kind == "csv":
                records = []
                for row in self.data["rows"]:
                    record = ET.SubElement(root, "row")
                    for i, header in enumerate(self.data["headers"]):
                        # XML element names must be valid; preserve original header as an attribute if needed.
                        name = re.sub(r"[^A-Za-z0-9_.-]", "_", header.strip())
                        if not name or not re.match(r"[A-Za-z_]", name[0]):
                            name = "field_" + name
                        child = ET.SubElement(record, name or f"field_{i+1}")
                        child.text = row[i] if i < len(row) else ""
            elif kind == "json":
                def add_json(parent, name, value):
                    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", str(name))
                    if not safe_name or not re.match(r"[A-Za-z_]", safe_name[0]):
                        safe_name = "item_" + safe_name
                    node = ET.SubElement(parent, safe_name or "item")
                    if isinstance(value, dict):
                        for k, v in value.items():
                            add_json(node, k, v)
                    elif isinstance(value, list):
                        for item in value:
                            add_json(node, "item", item)
                    elif value is not None:
                        node.text = str(value)
                    else:
                        node.set("type", "null")
                add_json(root, "data", self.data["content"])
            else:
                root.text = self.data["content"]
            ET.indent(root, space="  ")
            return ET.tostring(root, encoding="unicode", xml_declaration=True)
        raise ValueError("Target format tidak dikenal.")

    def save_file(self):
        if not self.data:
            messagebox.showwarning("Warning", "No file loaded!")
            return
        content = self.raw_text.get("1.0", "end-1c")
        try:
            # Parse edited raw text before saving so invalid structured data is not silently accepted.
            parsed = self.parse_content(self.current_format, content)
            filename = self.current_file
            if not filename:
                self.save_as_file(content)
                return
            with open(filename, "w", encoding="utf-8", newline="") as file:
                file.write(content)
            self.data = parsed
            self.update_all_views()
            self.update_file_info()
            self.set_status(f"Saved: {os.path.basename(filename)}")
            messagebox.showinfo("Success", f"File saved: {os.path.basename(filename)}")
        except Exception as exc:
            messagebox.showerror("Save Error", f"File tidak disimpan karena format tidak valid atau terjadi error:\n{exc}")

    def save_as_file(self, content=None):
        if content is None:
            if not self.data:
                messagebox.showwarning("Warning", "No file loaded!")
                return
            content = self.raw_text.get("1.0", "end-1c")
        fmt = self.current_format or "Text"
        extension = {"CSV": ".csv", "JSON": ".json", "XML": ".xml", "Text": ".txt"}.get(fmt, ".txt")
        filetypes = [(f"{fmt} files", f"*{extension}"), ("All files", "*.*")]
        filename = filedialog.asksaveasfilename(
            title="Save File As", filetypes=filetypes, defaultextension=extension
        )
        if not filename:
            return
        try:
            parsed = self.parse_content(fmt, content)
            with open(filename, "w", encoding="utf-8", newline="") as file:
                file.write(content)
            self.current_file = filename
            self.data = parsed
            self.update_file_info()
            self.update_all_views()
            self.set_status(f"Saved as: {os.path.basename(filename)}")
            messagebox.showinfo("Success", f"File saved as: {os.path.basename(filename)}")
        except Exception as exc:
            messagebox.showerror("Save Error", f"Cannot save file:\n{exc}")

    def jalankan(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = MultiFormatManager()
    app.jalankan()
