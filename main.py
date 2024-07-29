import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

class JsonViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JSON Viewer")
        self.geometry("800x600")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.load_button = ttk.Button(self, text="Load JSON File", command=self.load_json)
        self.load_button.pack(pady=10)
        
        self.tree = ttk.Treeview(self)
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                self.display_json(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file:\n{e}")
            
    def display_json(self, data, parent=""):
        if isinstance(data, dict):
            for key, value in data.items():
                node = self.tree.insert(parent, "end", text=key, open=True)
                self.display_json(value, node)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                item_node = self.tree.insert(parent, "end", text=f"[{index}]", open=True)
                self.display_json(item, item_node)
        else:
            self.tree.insert(parent, "end", text=str(data))

if __name__ == "__main__":
    app = JsonViewer()
    app.mainloop()

