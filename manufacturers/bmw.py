import os
import sys

# 프로젝트 루트 디렉토리를 sys.path에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_bmw(driver, df):
    url = 'https://parts-info.bmw.co.kr/'
    wait = WebDriverWait(driver, 10)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        try:
            driver.get(url)
            ignore_conditions = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.input')))
            if not ignore_conditions.is_selected():
                ignore_conditions.click()
            print("Ignore conditions selected.")
        except Exception as e:
            print(f"Error selecting ignore conditions: {e}")
            continue

        try:
            search_box = wait.until(EC.presence_of_element_located((By.ID, 'keyword')))
            search_box.clear()
            search_box.send_keys(part_number)
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"].btn-01')))
            search_button.click()

            result_row = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody.lh-search-tbody tr')))
            brand_result = result_row.find_element(By.CSS_SELECTOR, 'td.brand').text
            series = result_row.find_element(By.CSS_SELECTOR, 'td.series').text
            model = result_row.find_element(By.CSS_SELECTOR, 'td.model').text
            part = result_row.find_element(By.CSS_SELECTOR, 'td.part').text
            number = result_row.find_element(By.CSS_SELECTOR, 'td.number').text
            name = result_row.find_element(By.CSS_SELECTOR, 'td.name').text
            price = result_row.find_element(By.CSS_SELECTOR, 'td.price').text
        except Exception as e:
            print(f"No results found for part number {part_number}: {e}")
            brand_result = series = model = part = number = name = price = 'No result found'

        results.append([brand_result, series, model, part, number, name, price])
        print([brand_result, series, model, part, number, name, price])

    return results
