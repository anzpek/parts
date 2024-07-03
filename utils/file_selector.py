import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def select_file():
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    initial_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Excel files", "*.xlsx")], parent=root)
    root.destroy()
    return file_path

def show_popup(message, file_path=None):
    def on_close():
        if file_path:
            subprocess.Popen(['start', 'excel.exe', file_path], shell=True)

    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    messagebox.showinfo("알림", message, parent=root)
    root.destroy()
    on_close()
