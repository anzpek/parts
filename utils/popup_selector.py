import os
import sys
import tkinter as tk
from tkinter import ttk

# 프로젝트 루트 디렉토리를 sys.path에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

def select_brand():
    brand = None
    
    def set_brand(selected_brand):
        nonlocal brand
        brand = selected_brand
        root.quit()

    root = tk.Tk()
    root.title("자동차 브랜드 선택")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    ttk.Label(frame, text="자동차 브랜드를 선택하세요:", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=3, pady=10)

    brands = ["Hyundai_Kia", "Chevrolet", "Porsche", "Benz", "BMW", "Audi", "Tesla 개발중",  "Volkswagen", "Jeep 개발중", "Toyota", "Lexus", "Nissan", "KG(쌍용)", "Honda", "Peugeot"]

    for index, brand_name in enumerate(brands):
        row = index // 3 + 1  # Adjust row to account for the label
        column = index % 3
        ttk.Button(frame, text=brand_name, command=lambda b=brand_name: set_brand(b)).grid(row=row, column=column, padx=5, pady=5)

    root.update_idletasks()
    width = 450 #가로
    height = 350 #세로
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return brand

def select_execution_mode():
    mode = None
    
    def set_mode(selected_mode):
        nonlocal mode
        mode = selected_mode
        root.quit()

    root = tk.Tk()
    root.title("실행 모드 선택")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    ttk.Label(frame, text="실행 모드를 선택하세요:", font=("Helvetica", 14)).pack(pady=10)

    ttk.Button(frame, text="백그라운드 실행", command=lambda: set_mode("headless")).pack(pady=5)
    ttk.Button(frame, text="실제 브라우저 실행", command=lambda: set_mode("visible")).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return mode
