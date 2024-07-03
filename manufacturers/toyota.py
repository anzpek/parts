import os
import sys

# 프로젝트 루트 디렉토리를 sys.path에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_toyota(driver, df):
    url = 'https://www.toyota.co.kr/parts-information/'
    wait = WebDriverWait(driver, 10)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#keyword')))
        search_box.clear()
        search_box.send_keys(part_number)
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[class="css-1h73gvd ew2f4pu0"]')))
        search_button.click()

        try:
            result_row = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.css-139s1wz.ebuesx31')))
            brand_result = "Toyota"
            series = result_row.find_elements(By.CSS_SELECTOR, 'td')[0].text
            model = result_row.find_elements(By.CSS_SELECTOR, 'td')[1].text
            part = result_row.find_elements(By.CSS_SELECTOR, 'td')[3].text
            number = result_row.find_elements(By.CSS_SELECTOR, 'td')[2].text
            name = result_row.find_elements(By.CSS_SELECTOR, 'td')[4].text
            price = result_row.find_elements(By.CSS_SELECTOR, 'td')[5].text
        except Exception as e:
            print(f"No results found for part number {part_number}: {e}")
            brand_result = series = model = part = number = name = price = 'No result found'

        results.append([brand_result, series, model, part, number, name, price])
        print([brand_result, series, model, part, number, name, price])

    return results
