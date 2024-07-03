import os
import sys
import tkinter as tk
from tkinter import ttk

# 프로젝트 루트 디렉토리를 sys.path에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_hyundai_manufacturer():
    manufacturer = None
    
    def set_manufacturer(selected_manufacturer):
        nonlocal manufacturer
        manufacturer = selected_manufacturer
        root.quit()

    root = tk.Tk()
    root.title("제조사 선택")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    ttk.Label(frame, text="제조사를 선택하세요:", font=("Helvetica", 14)).pack(pady=10)

    ttk.Button(frame, text="현대", command=lambda: set_manufacturer("현대")).pack(pady=5)
    ttk.Button(frame, text="기아", command=lambda: set_manufacturer("기아")).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return manufacturer

def select_hyundai_search_mode():
    search_mode = None
    
    def set_search_mode(selected_mode):
        nonlocal search_mode
        search_mode = selected_mode
        root.quit()

    root = tk.Tk()
    root.title("검색 방식 선택")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    ttk.Label(frame, text="검색 방식을 선택하세요:", font=("Helvetica", 14)).pack(pady=10)

    ttk.Button(frame, text="일반검색", command=lambda: set_search_mode("normal")).pack(pady=5)
    ttk.Button(frame, text="부품번호로 검색", command=lambda: set_search_mode("ptno")).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return search_mode

def scrape_hyundai_kia(driver, df, search_mode, manufacturer):
    url = 'https://www.mobis-as.com/simple_search_part.do'
    wait = WebDriverWait(driver, 10)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)
        if search_mode == "normal":
            radio_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="how1"]')))
        elif search_mode == "ptno":
            radio_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="how2"]')))
        radio_button.click()

        if manufacturer == "현대":
            manufacturer_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="make1"]')))
        elif manufacturer == "기아":
            manufacturer_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="make2"]')))
        else:
            raise ValueError(f"Unknown manufacturer: {manufacturer}")
        
        manufacturer_button.click()

        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#searchNm2')))
        search_box.clear()
        search_box.send_keys(part_number)
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-red')))
        search_button.click()

        try:
            result_row = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[role="row"]')))
            part_number_result = result_row.find_element(By.CSS_SELECTOR, 'span.t-td[role="cell"] a').text
            part_name_korean = result_row.find_elements(By.CSS_SELECTOR, 'span.t-td[role="cell"]')[1].text
            part_name_english = result_row.find_elements(By.CSS_SELECTOR, 'span.t-td[role="cell"]')[2].text
            part_price = result_row.find_elements(By.CSS_SELECTOR, 'span.t-td[role="cell"]')[3].text.strip()
        except Exception as e:
            print(f"No results found for part number {part_number}: {e}")
            part_number_result = part_name_korean = part_name_english = part_price = 'No result found'

        results.append([manufacturer, '-', '-', part_name_korean, part_number_result, part_name_english, part_price])
        print([manufacturer, '-', '-', part_name_korean, part_number_result, part_name_english, part_price])

    return results