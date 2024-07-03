import tkinter as tk
from tkinter import ttk
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_porsche(driver, df):
    url = 'https://www.porsche.com/korea/ko/accessoriesandservice/porscheservice/vehicleinformation/independentworkshops/original-parts-search/default.ashx#m-174-resultr'
    wait = WebDriverWait(driver, 60)  # 검색 결과가 늦게 로드되므로 대기 시간을 60초로 설정
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)
        
        # 페이지가 완전히 로드되도록 충분한 시간 대기
        time.sleep(5)  # 로드 시간을 충분히 주기 위해 5초 대기

        # 부품 번호 입력
        try:
            part_input = wait.until(EC.presence_of_element_located((By.NAME, 'partno')))
            part_input.clear()
            part_input.send_keys(part_number)
            print(f"부품 번호 입력 완료: {part_number}")
        except TimeoutException:
            print(f"Timeout while entering part number: {part_number}")
            results.append(["포르쉐", part_number, "Timeout 발생", "", "", ""])
            continue

        # 검색 버튼 클릭
        try:
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.gui-btn.gui-link-with-article.m-174__search')))
            driver.execute_script("arguments[0].click();", search_button)
            print(f"검색 버튼 클릭 완료: {part_number}")
        except TimeoutException:
            print(f"Timeout while clicking search button for part number: {part_number}")
            results.append(["포르쉐", part_number, "Timeout 발생", "", "", ""])
            continue

        # 결과 대기
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > main > div.m-174.m-174-service-originalparts.module-container > div.m-174-table-container > div.m-174-table > div.m-174-table__content > div:nth-child(1) > div:nth-child(1)")))
            print("결과 로드 완료")

            part_number_result = driver.find_element(By.CSS_SELECTOR, "body > main > div.m-174.m-174-service-originalparts.module-container > div.m-174-table-container > div.m-174-table > div.m-174-table__content > div:nth-child(1) > div:nth-child(1)").text.strip()
            part_name = driver.find_element(By.CSS_SELECTOR, "body > main > div.m-174.m-174-service-originalparts.module-container > div.m-174-table-container > div.m-174-table > div.m-174-table__content > div:nth-child(1) > div:nth-child(2)").text.strip()
            part_price = driver.find_element(By.CSS_SELECTOR, "body > main > div.m-174.m-174-service-originalparts.module-container > div.m-174-table-container > div.m-174-table > div.m-174-table__content > div:nth-child(1) > div:nth-child(3)").text.strip()

            results.append(["포르쉐", "-", "-", "-", part_number_result, part_name, part_price])
            print(["포르쉐", "-", "-", "-", part_number_result, part_name, part_price])
        
        except TimeoutException:
            print(f"Timeout while retrieving results for part number: {part_number}")
            results.append(["포르쉐", part_number, "Timeout 발생", "", "", ""])
        except NoSuchElementException:
            print(f"No results found for part number: {part_number}")
            results.append(["포르쉐", part_number, "검색된 부품이 없습니다.", "", "", ""])
        except Exception as e:
            print(f"Error occurred while retrieving results for part number: {part_number}: {e}")
            results.append(["포르쉐", part_number, "에러 발생", "", "", ""])

    return results