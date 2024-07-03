import tkinter as tk
from tkinter import ttk
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def select_audi_year():
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

    year_options = ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]

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

def select_audi_model(year):
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
        "2016": ["A3 e-tron Sportback 1.4", "A4 45 TFSI", "A4 45 TFSI Premium", "A4 45 TFSI qu. Premium", "A4 45 TFSI qu. Sport", "A4 45 TFSI Sport", "A6 35 TDI", "A6 35 TDI PRMIUM"],
        "2017": ["A4 45 TFSI", "A4 45 TFSI Premium", "A4 45 TFSI qu. Sport", "A4 45 TFSI Sport", "A6 35 TDI", "A6 35 TDI PRMIUM", "A6 40 TFSI", "A6 40 TFSI PRMIUM", "A6 40 TFSI qu.", "A6 40 TFSI qu. PRMIUM"],
        "2018": ["A3 40 TFSI", "A3 40 TFSI Premium", "A4 30 TDI", "A4 30 TDI Premium", "A4 35 TDI", "A4 35 TDI Premium", "A4 35 TDI qu.", "A4 35 TDI qu. Premium", "A6 35 TDI", "A6 35 TDI PRMIUM", "A6 35 TDI qu.", "A6 35 TDI qu. PRMIUM", "A6 40 TFSI", "A6 40 TFSI PRMIUM"],
        "2019": ["A3 40 TFSI", "A4 40 TFSI", "A4 40 TFSI Premium", "A5 Cabriolet 45 TFSI qu. Premium", "A5 Coupe 45 TFSI qu. Premium", "A5 Sportback 45 TFSI qu. Premium", "A6 45 TFSI qu.", "A6 45 TFSI qu. Premium", "Q7 45 TFSI qu."],
        "2020": ["A3 40 TFSI", "A4 35 TDI Premium", "A4 40 TDI qu. Premium", "A4 40 TFSI", "A4 40 TFSI Premium", "A5 Cabriolet 45 TFSI qu. Premium", "A5 Coupe 45 TFSI qu. Premium", "A5 Sportback 40 TDI qu. Premium", "A5 Sportback 45 TFSI qu. Premium", "A6 40 TDI", "A6 40 TDI Premium", "A6 40 TDI qu. Premium", "A6 45 TDI qu. Premium", "A6 45 TFSI", "A6 45 TFSI Premium", "A6 45 TFSI qu.", "A6 45 TFSI qu. Premium", "A6 50 TDI qu. Premium", "A7 45 TDI qu. Premium", "A7 50 TDI qu. Premium", "A7 55 TFSI qu. Premium", "A8 50 TDI LWB qu.", "A8 50 TDI qu.", "A8 55 TFSI LWB qu.", "A8 60 TFSI LWB qu.", "e-tron 55 quattro", "Q2 35 TDI", "Q2 35 TDI Premium", "Q3 35 TDI", "Q3 35 TDI Premium", "Q3 SB 35 TDI", "Q3 SB 35 TDI Premium", "Q5 40 TDI qu.", "Q5 40 TDI qu. Premium", "Q5 45 TFSI qu. Premium", "Q5 50 TDI qu. Premium", "Q7 45 TFSI qu.", "Q8 50 TDI qu. Premium", "S6 TDI", "S7 TDI", "S8 LWB qu.", "SQ5 TDI"],
        "2021": ["A4 35 TDI", "A4 35 TDI Premium", "A4 40 TDI qu. Premium", "A4 40 TFSI", "A4 40 TFSI Premium", "A4 45 TFSI qu. Premium", "A5 Cabriolet 45 TFSI qu. Premium", "A5 Sportback 40 TDI qu. Premium", "A5 Sportback 40 TFSI qu.", "A5 Sportback 40 TFSI qu. Premium", "A5 Sportback 45 TFSI qu. Premium", "A6 40 TDI", "A6 40 TDI Premium", "A6 40 TDI qu. Premium", "A6 45 TDI qu. Premium", "A6 45 TFSI", "A6 45 TFSI Premium", "A6 45 TFSI qu. Premium", "A6 50 TDI qu. Premium", "A7 45 TDI qu. Premium", "A7 50 TDI qu. Premium", "A7 55 TFSI qu. Premium", "A8 50 TDI LWB qu.", "A8 50 TDI qu.", "A8 55 TFSI LWB qu.", "A8 60 TFSI LWB qu.", "Audi e-tron 55 e-tron qu.", "Audi e-tron Sportback 55 e-tron qu.", "Audi Q5 40 TDI qu. Premium", "Audi Q5 45 TFSI qu.", "Audi Q5 Sportback 40 TDI qu.", "Audi Q5 Sportback 45 TFSI qu.", "Audi Q5 Sportback 45 TFSI qu. Premium", "Audi RS Q8 quattro 4.0", "Audi RS5 Sportback quattro 2.9", "Audi SQ5 TFSI", "e-tron 50 qu.", "e-tron GT (350kw)", "e-tron GT RS (440kw)", "e-tron Sportback 50 qu.", "Q7 45 TDI qu.", "Q7 45 TDI qu. Premium", "Q7 50 TDI qu. Premium", "Q7 55 TFSI qu. Premium", "Q8 45 TDI qu. Premium", "Q8 50 TDI qu. Premium", "Q8 55 TFSI qu. Premium", "R8 V10 Performance", "S6 TDI", "S7 TDI", "S8 LWB qu.", "SQ5 TDI"],
        "2022": ["A3 40 TFSI", "A3 40 TFSI Premium", "A4 35 TDI Premium", "A4 40 TDI qu. Premium", "A4 40 TFSI", "A4 40 TFSI Premium", "A4 45 TFSI qu. Premium", "A5 Cabriolet 45 TFSI qu. Premium", "A5 Coupe 45 TFSI qu. Premium", "A5 Sportback 40 TDI qu. Premium", "A5 Sportback 40 TFSI qu.", "A5 Sportback 40 TFSI qu. Premium", "A5 Sportback 45 TFSI qu. Premium", "A6 40 TDI", "A6 40 TDI Premium", "A6 40 TDI qu. Premium", "A6 45 TDI qu. Premium", "A6 45 TFSI", "A6 45 TFSI Premium", "A6 50 TDI qu. Premium", "A7 45 TDI qu. Premium", "A7 50 TDI qu. Premium", "A8 50 TDI LWB qu.", "A8 50 TDI qu.", "A8 55 TFSI LWB qu.", "A8 60 TFSI LWB qu.", "e-tron S qu.", "e-tron Sportback 50 qu.", "e-tron Sportback S qu.", "Q3 35 TDI", "Q3 35 TDI Premium", "Q3 35 TDI qu. Premium", "Q3 Sportback 35 TDI", "Q3 Sportback 35 TDI Premium", "Q3 Sportback 35 TDI qu. Premium", "Q4 e-tron 40", "Q4 Sportback e-tron 40", "Q5 45 TFSI qu.", "Q5 45 TFSI qu. Premium", "Q5 Sportback 45 TFSI qu.", "Q5 Sportback 45 TFSI qu. Premium", "Q7 55 TFSI qu. Premium", "Q8 55 TFSI qu. Premium", "RS5", "RS6 Avant", "RS7", "S4 TFSI", "S5 TFSI Coupe", "S6 TDI", "S7 TDI", "S8 LWB qu.", "SQ5 Sportback TFSI qu.", "SQ5 TFSI"],
        "2023": ["Q2 2.0 TDI", "Q2 2.0 TDI Premium"],
        "2024": ["A4 40 TFSI", "A4 40 TFSI Premium", "A5 Cabriolet 45 TFSI qu. Premium", "A5 Coupe 45 TFSI qu. Premium", "A5 Sportback 40 TFSI qu.", "A5 Sportback 40 TFSI qu. Premium", "A5 Sportback 45 TFSI qu. Premium", "Q3 40 TFSI qu.", "Q3 40 TFSI qu. Premium", "Q3 Sportback 40 TFSI qu.", "Q3 Sportback 40 TFSI qu. Premium", "Q5 45 TFSI qu.", "Q5 45 TFSI qu. Premium", "Q5 Sportback 45 TFSI qu.", "Q5 Sportback 45 TFSI qu. Premium", "Q8 e-tron 50 qu", "Q8 e-tron 55 qu", "RS3", "RS6 Performance", "RS7 Performance", "S3 TFSI", "SQ5 Sportback TFSI qu.", "SQ8 e-tron"]
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

def scrape_audi(driver, df, year, model):
    url = 'https://www.audikoreaevent.co.kr/etc/component/index1.jsp'
    wait = WebDriverWait(driver, 5)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)

        # 연도 선택
        year_select = wait.until(EC.presence_of_element_located((By.ID, 'sYear')))
        year_options = year_select.find_elements(By.TAG_NAME, 'option')
        for option in year_options:
            if option.text == year:
                option.click()
                break

        # 모델 선택
        model_select = wait.until(EC.presence_of_element_located((By.ID, 'sModel')))
        model_options = model_select.find_elements(By.TAG_NAME, 'option')
        model_found = False
        for option in model_options:
            if option.text == model:
                option.click()
                model_found = True
                break

        if not model_found:
            print(f"해당 연도에 해당 모델명이 존재하지 않습니다: {model}")
            results.append(["아우디", year, model, part_number, "해당 모델 없음", "", "", ""])
            continue

        # 부품 번호 선택 및 입력
        key_select = wait.until(EC.presence_of_element_located((By.ID, 'sKey')))
        key_select.find_element(By.CSS_SELECTOR, "option[value='com_no']").click()

        part_input = wait.until(EC.presence_of_element_located((By.ID, 'sValue')))
        part_input.clear()
        part_input.send_keys(part_number)

        # 검색 버튼 클릭
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='검색']")))
        search_button.click()

        try:
            # 검색 결과가 로드될 때까지 기다리기
            wait.until(EC.presence_of_element_located((By.XPATH, "//td/b[text()='1']")))

            result_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
            rows = result_table.find_elements(By.TAG_NAME, 'tr')

            # "검색된 부품이 없습니다." 메시지가 나타나는지 확인
            if len(rows) < 2 or any('검색된 부품이 없습니다.' in row.text for row in rows):
                print(f"No results found for part number {part_number}")
                results.append(["아우디", year, model, part_number, "검색된 부품이 없습니다.", "", ""])
                continue

            # 첫 번째 행의 데이터 추출
            part_model = driver.find_element(By.CSS_SELECTOR, "#pop_comp > div > div.tbl_style02 > table > tbody > tr:nth-child(1) > td.m_name").text.strip()
            part_group = driver.find_element(By.CSS_SELECTOR, "#pop_comp > div > div.tbl_style02 > table > tbody > tr:nth-child(1) > td.m_group").text.strip()
            part_number_result = driver.find_element(By.CSS_SELECTOR, "#pop_comp > div > div.tbl_style02 > table > tbody > tr:nth-child(1) > td.m_no").text.strip()
            part_name_english = driver.find_element(By.CSS_SELECTOR, "#pop_comp > div > div.tbl_style02 > table > tbody > tr:nth-child(1) > td.m_enm").text.strip()
            part_name_korean = driver.find_element(By.CSS_SELECTOR, "#pop_comp > div > div.tbl_style02 > table > tbody > tr:nth-child(1) > td.m_knm").text.strip()
            part_price = driver.find_element(By.CSS_SELECTOR, "#pop_comp > div > div.tbl_style02 > table > tbody > tr:nth-child(1) > td.price").text.strip()

            results.append(["아우디", part_model, part_group, part_number_result, part_name_english, part_name_korean, part_price])
            print(["아우디", part_model, part_group, part_number_result, part_name_english, part_name_korean, part_price])
        
        except TimeoutException:
            print(f"Timeout while waiting for part number {part_number}")
            results.append(["아우디", model, year, part_number, "", "조회 결과 없음", ""])
        except Exception as e:
            print(f"Error occurred while searching for part number {part_number}: {e}")
            results.append(["아우디", year, model, part_number, "에러 발생", "", ""])

    return results