import tkinter as tk
from tkinter import ttk
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_lexus(driver, df):
    url = 'https://www.lexus.co.kr/service/part-price/'
    wait = WebDriverWait(driver, 10)  # 검색 결과가 빠르게 로드되므로 대기 시간을 30초로 설정
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)

        # 부품 번호 입력
        try:
            part_input = wait.until(EC.presence_of_element_located((By.ID, 'js-txfield-part')))
            part_input.clear()
            part_input.send_keys(part_number)
            print(f"부품 번호 입력 완료: {part_number}")
        except TimeoutException:
            print(f"Timeout while entering part number: {part_number}")
            results.append(["렉서스", part_number, "Timeout 발생", "", "", "", ""])
            continue

        # 검색 버튼 클릭
        try:
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]')))
            driver.execute_script("arguments[0].click();", search_button)
            print(f"검색 버튼 클릭 완료: {part_number}")
        except TimeoutException:
            print(f"Timeout while clicking search button for part number: {part_number}")
            results.append(["렉서스", part_number, "Timeout 발생", "", "", "", ""])
            continue

        # 결과 대기
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#el_content > section > div.tbl-wrap > table > tbody > tr:nth-child(1) > th > span:nth-child(2)")))
            print("결과 로드 완료")

            part_model = driver.find_element(By.CSS_SELECTOR, "#el_content > section > div.tbl-wrap > table > tbody > tr:nth-child(1) > th > span:nth-child(2)").text.strip()
            part_number_result = driver.find_element(By.CSS_SELECTOR, "#el_content > section > div.tbl-wrap > table > tbody > tr:nth-child(1) > td:nth-child(2) > span:nth-child(2)").text.strip()
            part_price = driver.find_element(By.CSS_SELECTOR, "#el_content > section > div.tbl-wrap > table > tbody > tr:nth-child(1) > td:nth-child(3) > span:nth-child(2)").text.strip()
            part_name_korean = driver.find_element(By.CSS_SELECTOR, "#el_content > section > div.tbl-wrap > table > tbody > tr:nth-child(1) > td:nth-child(4) > span:nth-child(2)").text.strip()
            part_name_english = driver.find_element(By.CSS_SELECTOR, "#el_content > section > div.tbl-wrap > table > tbody > tr:nth-child(1) > td:nth-child(5) > span:nth-child(2)").text.strip()

            results.append(["렉서스", part_model, "-", part_name_english, part_number_result, part_name_korean, part_price])
            print(["렉서스", part_model, "-", part_name_english, part_number_result, part_name_korean, part_price])
        
        except TimeoutException:
            print(f"Timeout while retrieving results for part number: {part_number}")
            results.append(["렉서스", part_number, "Timeout 발생", "", "", "", ""])
        except NoSuchElementException:
            print(f"No results found for part number: {part_number}")
            results.append(["렉서스", part_number, "검색된 부품이 없습니다.", "", "", "", ""])
        except Exception as e:
            print(f"Error occurred while retrieving results for part number: {part_number}: {e}")
            results.append(["렉서스", part_number, "에러 발생", "", "", "", ""])

    return results
