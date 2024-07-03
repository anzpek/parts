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

def select_chevrolet_model():
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
        "(올뉴) 아베오/트랙스", "ACDelco", "G2X", "누비라/누비라 II", "뉴마티즈", 
        "다마스/라보", "더 넥스트 스파크", "더뉴말리부", "라노스", "라세티",
        "레간자", "레조", "마티즈", "매그너스", "베리타스", "볼트", 
        "볼트 EV", "스테이츠맨", "스파크/스파크EV", "씨에로/넥시아/르망", 
        "아카디아", "알페온/말리부", "액세서리", "에스페로", "올뉴말리부", 
        "올뉴크루즈", "윈스톰/캡티바", "이쿼녹스", "이쿼녹스1.5", "임팔라", 
        "젠트라", "카마로", "카마로 SS", "칼로스", "콜로라도", "콜벳", 
        "크루즈/올란도", "타호", "토스카", "트래버스", "트레일블레이저", 
        "트레일블레이저/트랙스", "티코", "프린스/브로엄/살롱"
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

def select_chevrolet_search_type():
    search_type = None
    
    def set_search_type(selected_type):
        nonlocal search_type
        search_type = selected_type
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

    ttk.Button(frame, text="부품명", command=lambda: set_search_type("asCodeDesc")).pack(pady=5)
    ttk.Button(frame, text="부품번호", command=lambda: set_search_type("asCode")).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return search_type

def scrape_chevrolet(driver, df, chevrolet_model, chevrolet_search_type):
    url = 'https://www.chevrolet.co.kr/chevy/part-information-price.gm'
    wait = WebDriverWait(driver, 10)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)

        model_select = wait.until(EC.presence_of_element_located((By.ID, 'mdl')))
        for option in model_select.find_elements(By.TAG_NAME, 'option'):
            if option.text == chevrolet_model:
                option.click()
                break

        search_type_select = wait.until(EC.presence_of_element_located((By.ID, 'searchCol')))
        for option in search_type_select.find_elements(By.TAG_NAME, 'option'):
            if option.get_attribute('value') == chevrolet_search_type:
                option.click()
                break

        search_box = wait.until(EC.presence_of_element_located((By.ID, 'searchVal')))
        search_box.clear()
        search_box.send_keys(part_number)
        search_button = wait.until(EC.element_to_be_clickable((By.ID, 'buttonSelect')))
        search_button.click()

        try:
            result_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
            rows = result_table.find_elements(By.TAG_NAME, 'tr')

            if len(rows) == 2 and "게시물이 없습니다." in rows[1].text:
                raise Exception(f"No results found for part number {part_number}")

            part_name_korean = rows[1].find_elements(By.TAG_NAME, 'td')[1].text.strip()
            part_number_result = rows[1].find_elements(By.TAG_NAME, 'td')[2].text.strip()
            part_price = rows[1].find_elements(By.TAG_NAME, 'td')[4].text.strip()
            part_name_english = '-'
        except Exception as e:
            print(f"No results found for part number {part_number}: {e}")
            part_name_korean = part_number_result = part_price = part_name_english = 'No result found'

        results.append(["쉐보레", chevrolet_model, '-', part_name_korean, part_number_result, part_name_korean, part_price])
        print(["쉐보레", chevrolet_model, '-', part_name_korean, part_number_result, part_name_korean, part_price])

    return results

