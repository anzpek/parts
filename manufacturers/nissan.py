import tkinter as tk
from tkinter import ttk
from tkinter.tix import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def select_nissan_model():
    model = None

    def set_model(selected_model):
        nonlocal model
        model = selected_model
        root.quit()

    root = tk.Tk()
    root.title("모델 선택")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    model_options = [
        "370Z", "ALTIMA 2.0", "ALTIMA 2.5", "ALTIMA 2.5(S)", "ALTIMA 2.5(T)", "ALTIMA 2.5(T)_PT", "ALTIMA 3.5",
        "ALTIMA 3.5(PT)", "ALTIMA 3.5(T)", "ALTIMA GREY", "CUBE GREY", "CUBE S", "CUBE SL", "CUBE US", "GT-R",
        "GT-R Black", "JUKE GREY", "JUKE S", "JUKE SV", "LEAF", "LEAF SL", "MARCH GREY", "MAXIMA", "MURANO",
        "MURANO HEV", "MURANO Hybrid", "MURANO US", "New ALTIMA 2.0 Turbo", "New ALTIMA 2.5", "New LEAF S",
        "New LEAF SL", "NEW MAXIMA", "PATHFINDER", "PATHFINDER MC", "QASHQAI S", "QASHQAI SL", "ROGUE 2WD",
        "ROGUE 4WD Deluxe", "ROGUE 4WD PRE", "ROGUE GREY", "WINGROAD GREY", "X-Trail"
    ]

    ttk.Label(frame, text="모델을 선택하세요:", font=("Helvetica", 14)).pack(pady=10)
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

def select_nissan_search_type():
    search_type = None

    def set_search_type(selected_search_type):
        nonlocal search_type
        search_type = selected_search_type
        root.quit()

    root = tk.Tk()
    root.title("검색 유형 선택")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    search_type_options = ["부품번호", "부품명"]

    ttk.Label(frame, text="검색 유형을 선택하세요:", font=("Helvetica", 14)).pack(pady=10)
    search_type_combobox = ttk.Combobox(frame, values=search_type_options, font=("Helvetica", 12))
    search_type_combobox.pack(pady=10)
    
    ttk.Button(frame, text="선택", command=lambda: set_search_type(search_type_combobox.get())).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return search_type

def scrape_nissan(driver, df, model, search_type):
    url = 'http://provider.nissan.co.kr/parts_price/index.asp'
    wait = WebDriverWait(driver, 20)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)
        time.sleep(0.5)
        # 모델 선택
        try:
            model_select = wait.until(EC.presence_of_element_located((By.ID, 'sel_cate1')))
            model_options = model_select.find_elements(By.TAG_NAME, 'option')
            model_found = False
            for option in model_options:
                if option.text == model:
                    option.click()
                    model_found = True
                    break
            if not model_found:
                print(f"Model not found: {model}")
                results.append(["닛산", model, "-", part_number, "모델 선택 실패", "", "", ""])
                continue
        except TimeoutException:
            print(f"Timeout while selecting model: {model}")
            results.append(["닛산", model, "-", part_number, "Timeout 발생", "", "", ""])
            continue

        # 검색 유형 선택
        try:
            search_type_select = wait.until(EC.presence_of_element_located((By.ID, 'sel_cate3')))
            search_type_options = search_type_select.find_elements(By.TAG_NAME, 'option')
            search_type_found = False
            for option in search_type_options:
                if option.text == search_type:
                    option.click()
                    search_type_found = True
                    break
            if not search_type_found:
                print(f"Search type not found: {search_type}")
                results.append(["닛산", model, "-", part_number, "검색 유형 선택 실패", "", "", ""])
                continue

        except TimeoutException:
            print(f"Timeout while selecting search type: {search_type}")
            results.append(["닛산", model, "-", part_number, "Timeout 발생", "", "", ""])
            continue

        # 부품 번호 입력
        try:
            part_input = wait.until(EC.presence_of_element_located((By.ID, 'sel_text')))
            part_input.clear()
            part_input.send_keys(part_number)
        except TimeoutException:
            print(f"Timeout while entering part number: {part_number}")
            results.append(["닛산", model, "-", part_number, "Timeout 발생", "", "", ""])
            continue

        # 검색 버튼 클릭
        try:
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_search")))
            search_button.click()
        except TimeoutException:
            print(f"Timeout while clicking search button for part number: {part_number}")
            results.append(["닛산", model, "-", part_number, "Timeout 발생", "", "", ""])
            continue
        time.sleep(1)
        # 검색 결과 가져오기
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content > div.parts_price_list > table > tbody > tr:nth-child(1) > td:nth-child(1)")))

            model_name = driver.find_element(By.CSS_SELECTOR, "#content > div.parts_price_list > table > tbody > tr:nth-child(1) > td:nth-child(1)").text.strip()
            category = driver.find_element(By.CSS_SELECTOR, "#content > div.parts_price_list > table > tbody > tr:nth-child(1) > td:nth-child(2)").text.strip()
            part_name_english = driver.find_element(By.CSS_SELECTOR, "#content > div.parts_price_list > table > tbody > tr:nth-child(1) > td:nth-child(3)").text.strip()
            part_name_korean = driver.find_element(By.CSS_SELECTOR, "#content > div.parts_price_list > table > tbody > tr:nth-child(1) > td:nth-child(4)").text.strip()
            part_number_result = driver.find_element(By.CSS_SELECTOR, "#content > div.parts_price_list > table > tbody > tr:nth-child(1) > td:nth-child(5)").text.strip()
            part_price = driver.find_element(By.CSS_SELECTOR, "#content > div.parts_price_list > table > tbody > tr:nth-child(1) > td:nth-child(6)").text.strip()

            results.append(["닛산", model_name, "-", part_name_english, part_number_result, part_name_korean, part_price])
            print(["닛산", model_name, "-", part_name_english, part_number_result, part_name_korean, part_price])
        
        except TimeoutException:
            print(f"Timeout while retrieving results for part number: {part_number}")
            results.append(["닛산", model, "-", part_number, "Timeout 발생", "", "", ""])
        except NoSuchElementException:
            print(f"No results found for part number: {part_number}")
            results.append(["닛산", model, "-", part_number, "검색된 부품이 없습니다.", "", "", ""])
        except Exception as e:
            print(f"Error occurred while retrieving results for part number: {part_number}: {e}")
            results.append(["닛산", model, "-", part_number, "에러 발생", "", "", ""])

    return results