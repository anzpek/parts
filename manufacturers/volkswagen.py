import tkinter as tk
from tkinter import ttk
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def select_volkswagen_year():
    year = None

    def set_year(selected_year):
        nonlocal year
        year = selected_year
        root.quit()

    root = tk.Tk()
    root.title("연도 선택")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    year_options = ["2014", "2015", "2016", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]

    ttk.Label(frame, text="연도를 선택하세요:", font=("Helvetica", 14)).pack(pady=10)
    year_combobox = ttk.Combobox(frame, values=year_options, font=("Helvetica", 12))
    year_combobox.pack(pady=10)
    
    ttk.Button(frame, text="선택", command=lambda: set_year(year_combobox.get())).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return year

def select_volkswagen_model(year):
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

    model_options_by_year = {
        "2014": ["CC 2.0 TDI 4Motion", "CC 2.0 TDI BlueMotion", "CC 2.0 TSI", "Golf 1.6 TDI BlueMotion", "Golf 2.0 TDI", "Golf Cabriolet 2.0 TDI BlueMotion", "Jetta 1.6 TDI BlueMotion", "Jetta 2.0 TDI", "Passat 2.0 TDI", "Passat 2.5", "Phaeton 3.0 TDI", "Phaeton 4.2", "Polo 1.6 TDI", "Scirocco R", "Scirocco R-Line", "The Beetle 2.0 TDI", "Tiguan 2.0 TDI BlueMotion", "Touareg 3.0 TDI BlueMotion", "Touareg 4.2 TDI"],
        "2015": ["CC 2.0 TDI BlueMotion", "CC 2.0 TSI", "Golf 1.4 TSI", "Golf 1.6 TDI BlueMotion", "Golf 2.0 TDI", "Golf GTD 2.0 TDI", "Golf GTI  2.0 TSI", "Passat 1.8 TSI", "Passat 2.0 TDI", "Phaeton 3.0 TDI", "Phaeton 4.2", "Scirocco R-Line", "The Beetle 2.0 TDI", "Tiguan 2.0 TDI BlueMotion"],
        "2016": ["CC 2.0 TDI GP BMT", "CC 2.0 TDI GP BMT R-LINE", "CC 2.0 TSI GP", "Golf  A7 2.0 GTD EXTREM", "Golf  A7 2.0 GTI", "Golf  A7 2.0 GTI EXTREM", "Golf A7 1.4 TSI BMT", "Golf A7 1.4 TSI BMT REPRMN", "Golf A7 2.0 TDI BMT", "Golf A7 2.0 TDI BMT PRM", "Golf A7 2.0 TDI BMT R-LINE", "Golf A7 2.0 TDI BMT REPRM", "Jetta 6 FL 2.0 TDI 110PS", "Jetta 6 FL 2.0 TDI 150PS", "Passat 1.8 TSI GP", "Polo 5 FL 1.4 TDI BMT", "Polo 5 FL 1.4 TDI BMT PRM", "The Beetle 2.0 TDI", "The Beetle 2.0 TDI PRM", "Tiguan 2.0 TDI BMT", "Tiguan 2.0 TDI BMT PRM", "Tiguan 2.0 TDI BMT R-LINE", "Touareg 3.0 GP TDI BMT", "Touareg 3.0 GP TDI BMT EXCLU", "Touareg 3.0 GP TDI BMT R-LINE"],
        "2018": ["Arteon 2.0 TDI PRM", "Arteon 2.0 TDI PRSTG", "Passat 2.0 TSI GP", "Tiguan 2.0 TDI 4M PRSTG", "Tiguan 2.0 TDI PRM", "Tiguan 2.0 TDI PRSTG"],
        "2019": ["Arteon 2.0 TDI PRM", "Arteon 2.0 TDI PRSTG"],
        "2020": ["Arteon 2.0 TDI 4M PRESTIGE-PRT", "Arteon 2.0 TDI PRESTIGE-PRT", "Arteon 2.0 TDI PRM", "Tiguan 2.0 TDI PRM", "Tiguan 2.0 TDI PRSTG", "Tiguan Allspace 2.0 TDI PRESTIGE-PRT"],
        "2021": ["Jetta 1.4 TSI PRESTIGE-PRT", "Jetta 1.4 TSI PRM", "Passat GT 2.0 TDI 4Motion PRESTIGE-PRT", "Passat GT 2.0 TDI PRESTIGE-PRT", "Passat GT 2.0 TDI PRM", "T-Roc 2.0 TDI PRESTIGE-PRT", "T-Roc 2.0 TDI PRM", "T-Roc 2.0 TDI Style", "Tiguan 2 PA 2.0 TDI 4M PRM", "Tiguan 2 PA 2.0 TDI 4M PRT", "Tiguan 2 PA 2.0 TDI PRM", "Tiguan 2 PA 2.0 TDI PRT", "Touareg 4.0 TDI PRESTIGE-PRT"],
        "2022": ["Arteon 8 PA 2.0 TDI 4M PRESTIGE-PRT", "Arteon 8 PA 2.0 TDI 4M R-LINE-RLN", "Arteon Prestige", "Golf 2.0 BlueMotion Technology Premium", "Golf 2.0 BlueMotion Technology Prestige", "Golf 2.0 TSI 180kW GTI", "ID.4 77kWh PRO", "Passat 2.0 TDI 147kW 4Motion Prestige", "Tiguan 2.0 TSI 137kW 2WD Prestige", "Touareg 3 3.0 TDI PRESTIGE-PRT", "Touareg 3.0 TDI 210kW Premium", "Touareg 3.0 TDI 210kW Prestige"],
        "2023": ["Arteon 8 PA 2.0 TDI 4M PRT", "Arteon 8 PA 2.0 TDI 4M RLN", "Arteon 8 PA 2.0 TDI PRT", "Golf 8 2.0 GTI", "Golf 8 2.0 TDI PRM", "Golf 8 2.0 TDI PRT", "ID.4 77kWh", "ID.4 77kWh PRO", "Jetta 7 PA 1.5 TSI PRESTIGE-PRT", "Jetta 7 PA 1.5 TSI PRM", "Jetta 7 PA 1.5 TSI PRT", "Tiguan 2 PA 2.0 TDI 4M PRT", "Tiguan 2 PA 2.0 TDI PRM", "Tiguan 2 PA 2.0 TDI PRT", "Tiguan Allspace 2 PA 2.0 TDI PRM", "Tiguan Allspace 2 PA 2.0 TDI PRT", "Tiguan Allspace 2 PA 2.0 TSI PRT", "Touareg 3 3.0 TDI PRM", "Touareg 3 3.0 TDI PRT", "Touareg 3 3.0 TDI RLN"],
        "2024": ["Golf 8 2.0 GTI"]
    }

    ttk.Label(frame, text=f"{year}년도 모델을 선택하세요:", font=("Helvetica", 14)).pack(pady=10)
    model_combobox = ttk.Combobox(frame, values=model_options_by_year[year], font=("Helvetica", 12))
    model_combobox.pack(pady=10)
    
    ttk.Button(frame, text="선택", command=lambda: set_model(model_combobox.get())).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return model

def scrape_volkswagen(driver, df, year, model):
    url = 'https://www.vwkr.co.kr/GenuinePartsList/index.jsp'
    wait = WebDriverWait(driver, 20)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)

        # 연도 선택
        try:
            year_select = wait.until(EC.presence_of_element_located((By.ID, 'smy')))
            year_options = year_select.find_elements(By.TAG_NAME, 'option')
            for option in year_options:
                if option.text == year:
                    option.click()
                    break
        except TimeoutException:
            print(f"Timeout while selecting year: {year}")
            results.append(["폭스바겐", year, model, part_number, "Timeout 발생", "", ""])
            continue

        # 모델 선택
        try:
            model_select = wait.until(EC.presence_of_element_located((By.ID, 'smn')))
            model_options = model_select.find_elements(By.TAG_NAME, 'option')
            model_found = False
            for option in model_options:
                if option.text == model:
                    option.click()
                    model_found = True
                    break
            if not model_found:
                print(f"해당 연도에 해당 모델명이 존재하지 않습니다: {model}")
                results.append(["폭스바겐", year, model, part_number, "해당 모델 없음", "", ""])
                continue
        except TimeoutException:
            print(f"Timeout while selecting model: {model}")
            results.append(["폭스바겐", year, model, part_number, "Timeout 발생", "", ""])
            continue

        # 부품 번호 입력
        try:
            part_input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
            part_input.clear()
            part_input.send_keys(part_number)
        except TimeoutException:
            print(f"Timeout while entering part number: {part_number}")
            results.append(["폭스바겐", year, model, part_number, "Timeout 발생", "", ""])
            continue

        # 검색 버튼 클릭
        try:
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-search")))
            search_button.click()
        except TimeoutException:
            print(f"Timeout while clicking search button for part number: {part_number}")
            results.append(["폭스바겐", year, model, part_number, "Timeout 발생", "", ""])
            continue

        # 검색 결과 가져오기
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#wrap-genuine > table > tbody > tr > td:nth-child(2)")))

            part_model = driver.find_element(By.CSS_SELECTOR, "#wrap-genuine > table > tbody > tr > td:nth-child(2)").text.strip()
            part_number_result = driver.find_element(By.CSS_SELECTOR, "#wrap-genuine > table > tbody > tr > td:nth-child(3)").text.strip()
            part_group = driver.find_element(By.CSS_SELECTOR, "#wrap-genuine > table > tbody > tr > td:nth-child(4)").text.strip()
            part_name_english = driver.find_element(By.CSS_SELECTOR, "#wrap-genuine > table > tbody > tr > td:nth-child(5)").text.strip()
            part_name_korean = driver.find_element(By.CSS_SELECTOR, "#wrap-genuine > table > tbody > tr > td.kor").text.strip()
            sub_part_number = driver.find_element(By.CSS_SELECTOR, "#wrap-genuine > table > tbody > tr > td:nth-child(7)").text.strip()
            part_price = driver.find_element(By.CSS_SELECTOR, "#wrap-genuine > table > tbody > tr > td.price").text.strip()

            results.append([part_model, part_group, part_number_result, part_name_english, part_name_korean, sub_part_number, part_price])
            print([part_model, part_group, part_number_result, part_name_english, part_name_korean, sub_part_number, part_price])
        
        except TimeoutException:
            print(f"Timeout while retrieving results for part number: {part_number}")
            results.append(["폭스바겐", year, model, part_number, "Timeout 발생", "", ""])
        except NoSuchElementException:
            print(f"No results found for part number: {part_number}")
            results.append(["폭스바겐", year, model, part_number, "검색된 부품이 없습니다.", "", ""])
        except Exception as e:
            print(f"Error occurred while retrieving results for part number: {part_number}: {e}")
            results.append(["폭스바겐", year, model, part_number, "에러 발생", "", ""])

    return results