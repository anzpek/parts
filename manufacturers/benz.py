import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, ttk
import time

# 프로젝트 루트 디렉토리를 sys.path에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def select_benz_model():
    model = None

    def set_model(selected_model):
        nonlocal model
        model = selected_model
        root.quit()

    root = tk.Tk()
    root.title("차종 선택")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    model_options = [
        "전체", "A-Class", "B-Class", "C-Class", "CLA-Class", "CL-Class", 
        "CLK-Class", "CLS-Class", "E-Class", "EQ", "G-Class",
        "GLA-Class", "GLB-Class", "GLC-Class", "GL-Class", "GLE-Class",
        "GLK-Class", "GLS-Class", "GT", "Maybach", "M-Class",
        "R-Class", "S-Class", "SL-Class", "SLK-Class", "SLR-Class",
        "SLS-Class", "Sprinter", "공통", "기타"
    ]

    ttk.Label(frame, text="차종을 선택하세요:", font=("Helvetica", 14)).pack(pady=10)

    model_combobox = ttk.Combobox(frame, values=model_options, font=("Helvetica", 12))
    model_combobox.pack(pady=10)
    
    ttk.Button(frame, text="선택", command=lambda: set_model(model_combobox.get())).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return model

def scrape_benz(driver, df, model):
    url = 'https://parts-price.mercedes-benz.co.kr/'
    wait = WebDriverWait(driver, 10)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)

        try:
            # 모델 선택
            wait.until(EC.presence_of_element_located((By.ID, 'classChange')))
            js_script = f"""
            var select = document.getElementById('classChange');
            select.value = '{model}';
            var event = new Event('change');
            select.dispatchEvent(event);
            """
            driver.execute_script(js_script)
            print(f"Model selected: {model}")

            search_box = wait.until(EC.presence_of_element_located((By.ID, 'patscodename')))
            search_box.clear()
            search_box.send_keys(part_number)
            search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn_search')))
            search_button.click()

            try:
                result_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
                rows = wait.until(lambda driver: result_table.find_elements(By.TAG_NAME, 'tr'))

                if len(rows) == 0:
                    raise Exception(f"No results found for part number {part_number}")

                part_number_result = rows[0].find_elements(By.TAG_NAME, 'td')[1].text.strip()
                part_name_korean = rows[0].find_elements(By.TAG_NAME, 'td')[2].text.strip()
                part_name_english = rows[0].find_elements(By.TAG_NAME, 'td')[3].text.strip()
                part_price = rows[0].find_elements(By.TAG_NAME, 'td')[6].text.strip()
                car_model = rows[0].find_elements(By.TAG_NAME, 'td')[7].text.strip()
            except Exception as e:
                print(f"No results found for part number {part_number}: {e}")
                part_number_result = part_name_korean = part_name_english = part_price = car_model = 'No result found'

            results.append(["벤츠", model, car_model, part_name_korean, part_number_result, part_name_english, part_price])
            print(["벤츠", model, car_model, part_name_korean, part_number_result, part_name_english, part_price])
        
        except Exception as e:
            print(f"Error processing part number {part_number}: {e}")
            results.append(["벤츠", model, "-", "Error", part_number, "Error", "Error"])

    return results