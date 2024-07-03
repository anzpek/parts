import os
import sys
import tkinter as tk
import time
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_argument('--proxy-server=http://YOUR_PROXY_SERVER:PORT')

def select_tesla_country():
    country = None
    
    def set_country(selected_country):
        nonlocal country
        country = selected_country
        root.quit()

    root = tk.Tk()
    root.title("Select Country")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    country_options = [
        "South Korea"
    ]

    ttk.Label(frame, text="Select a country:", font=("Helvetica", 14)).pack(pady=10)

    country_combobox = ttk.Combobox(frame, values=country_options, font=("Helvetica", 12))
    country_combobox.pack(pady=10)
    
    ttk.Button(frame, text="Select", command=lambda: set_country(country_combobox.get())).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return country

def select_tesla_product():
    product = None
    
    def set_product(selected_product):
        nonlocal product
        product = selected_product
        root.quit()

    root = tk.Tk()
    root.title("Select Product")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    product_options = ["Tesla Vehicles"]

    ttk.Label(frame, text="Select a product:", font=("Helvetica", 14)).pack(pady=10)

    product_combobox = ttk.Combobox(frame, values=product_options, font=("Helvetica", 12))
    product_combobox.pack(pady=10)
    
    ttk.Button(frame, text="Select", command=lambda: set_product(product_combobox.get())).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return product

def select_tesla_model():
    model = None
    
    def set_model(selected_model):
        nonlocal model
        model = selected_model
        root.quit()

    root = tk.Tk()
    root.title("Select Model")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    model_options = ["Model S", "Model 3", "Model X", "Model Y"]

    ttk.Label(frame, text="Select a model:", font=("Helvetica", 14)).pack(pady=10)

    model_combobox = ttk.Combobox(frame, values=model_options, font=("Helvetica", 12))
    model_combobox.pack(pady=10)
    
    ttk.Button(frame, text="Select", command=lambda: set_model(model_combobox.get())).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return model

def select_tesla_catalog(model):
    if model == "Model Y":
        return None
    
    catalog = None
    
    def set_catalog(selected_catalog):
        nonlocal catalog
        catalog = selected_catalog
        root.quit()

    root = tk.Tk()
    root.title("Select Catalog")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    catalog_options = []
    if model == "Model S":
        catalog_options = ["Model S Apr 2016 - Jan 2021", "Model S Feb 2012 - Mar 2016", "Model S Feb 2021"]
    elif model == "Model 3":
        catalog_options = ["Model 3 Jun 2017 - Aug 2023", "Model 3 Sep 2023"]
    elif model == "Model X":
        catalog_options = ["Model X Sep 2015 - Feb 2021", "Model X Mar 2021"]
    
    ttk.Label(frame, text="Select a catalog:", font=("Helvetica", 14)).pack(pady=10)

    catalog_combobox = ttk.Combobox(frame, values=catalog_options, font=("Helvetica", 12))
    catalog_combobox.pack(pady=10)
    
    ttk.Button(frame, text="Select", command=lambda: set_catalog(catalog_combobox.get())).pack(pady=5)

    root.update_idletasks()
    width = max([frame.winfo_reqwidth()] + [child.winfo_reqwidth() for child in frame.winfo_children()]) + 40
    height = sum(child.winfo_reqheight() for child in frame.winfo_children()) + 100
    root.geometry(f"{width}x{height}")

    root.mainloop()
    root.destroy()
    
    return catalog

def scrape_tesla(driver, df, country, product, model, catalog):
    url = 'https://epc.tesla.com/ko-KR/catalogs'
    wait = WebDriverWait(driver, 30)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)

        # 로딩 스피너가 사라질 때까지 기다림
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.loader')))

        # 국가 선택
        country_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'select.tds-select-input')))
        country_select.click()
        for option in country_select.find_elements(By.TAG_NAME, 'option'):
            if "South Korea" in option.text:
                option.click()
                break

        # 제품 선택 창이 나타날 때까지 기다림
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'select.tds-select-input')) > 1)
        product_select = driver.find_elements(By.CSS_SELECTOR, 'select.tds-select-input')[1]
        product_select.click()
        for option in product_select.find_elements(By.TAG_NAME, 'option'):
            if "Tesla Vehicles" in option.text:
                option.click()
                break

        # 차종 선택 창이 나타날 때까지 기다림
        wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'select.tds-select-input')) > 2)
        model_select = driver.find_elements(By.CSS_SELECTOR, 'select.tds-select-input')[2]
        model_select.click()
        for option in model_select.find_elements(By.TAG_NAME, 'option'):
            if model in option.text:
                option.click()
                break

        if model == "Model Y":
            # Model Y를 선택한 경우 바로 계속하다 버튼을 클릭
            continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
            continue_button.click()
        else:
            # 카탈로그 선택 창이 나타날 때까지 기다림
            wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'select.tds-select-input')) > 3)
            catalog_select = driver.find_elements(By.CSS_SELECTOR, 'select.tds-select-input')[3]
            catalog_select.click()
            for option in catalog_select.find_elements(By.TAG_NAME, 'option'):
                if catalog in option.text:
                    option.click()
                    break

            # 계속하다 버튼을 클릭
            continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
            continue_button.click()

        # 페이지가 완전히 로드될 때까지 기다림
        time.sleep(5)

        # 부품 검색창이 나타날 때까지 기다림
        search_box = wait.until(EC.presence_of_element_located((By.ID, 'tds-search-input')))

        # 부품 번호를 JavaScript로 입력하고 이벤트 트리거
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", search_box, part_number)

        # 검색 버튼을 클릭
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg.tds-search-icon')))
        search_button.click()

        # 부품 번호 확인이 나타날 때까지 기다림
        search_result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.tds-search-result')))
        search_result.click()

        # 결과 테이블이 나타날 때까지 기다림
        results_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.tds-table')))
        rows = results_table.find_elements(By.TAG_NAME, 'tr')

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if cells and part_number in cells[2].text:  # 부품 번호가 있는 열을 확인
                result = [cell.text for cell in cells]
                results.append(result)
                break

    return results