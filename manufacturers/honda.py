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

def scrape_honda(driver, df):
    url = 'https://auto.hondakorea.co.kr/service/part-info'
    wait = WebDriverWait(driver, 20)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)
        
        # 검색 유형 선택: 부품번호
        try:
            js_script = """
            document.querySelector('select[name="scKey"]').value = 'parNum';
            var event = new Event('change');
            document.querySelector('select[name="scKey"]').dispatchEvent(event);
            """
            driver.execute_script(js_script)
            print("검색 유형 선택 완료: 부품번호")
        except Exception as e:
            print(f"JavaScript로 검색 유형을 선택하는 데 실패했습니다: {e}")
            results.append(["혼다", "-", "-", part_number, "검색 유형 선택 실패", "", "", ""])
            continue

        # 부품 번호 입력
        try:
            js_script = f"""
            document.querySelector('#scVal').value = '{part_number}';
            """
            driver.execute_script(js_script)
            print(f"부품 번호 입력 완료: {part_number}")
        except Exception as e:
            print(f"JavaScript로 부품 번호를 입력하는 데 실패했습니다: {e}")
            results.append(["혼다", "-", "-", part_number, "부품 번호 입력 실패", "", "", ""])
            continue

        # 검색 버튼 클릭
        try:
            js_script = """
            document.querySelector('button.btnSearch').click();
            """
            driver.execute_script(js_script)
            print(f"검색 버튼 클릭 완료: {part_number}")
        except Exception as e:
            print(f"JavaScript로 검색 버튼을 클릭하는 데 실패했습니다: {e}")
            results.append(["혼다", "-", "-", part_number, "검색 버튼 클릭 실패", "", "", ""])
            continue

        # 검색 결과 가져오기
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#partList')))
            
            # 모델명
            part_model = driver.find_element(By.CSS_SELECTOR, '#partList > td:nth-child(1)').text.strip()
            print(f"모델명 가져오기 완료: {part_model}")
            
            # 부품번호
            part_number_result = driver.find_element(By.CSS_SELECTOR, '#partList > td:nth-child(2)').text.strip()
            print(f"부품번호 가져오기 완료: {part_number_result}")
            
            # 부품명 (한글)
            part_name_korean = driver.find_element(By.CSS_SELECTOR, '#partList > td:nth-child(3)').text.strip()
            print(f"부품명(한글) 가져오기 완료: {part_name_korean}")
            
            # 부품명 (영문)
            part_name_english = driver.find_element(By.CSS_SELECTOR, '#partList > td:nth-child(4)').text.strip()
            print(f"부품명(영문) 가져오기 완료: {part_name_english}")
            
            # 부품 가격 (JavaScript로 가져오기)
            js_script = """
            return document.querySelector('#partList > td:nth-child(5)').innerHTML.trim();
            """
            part_price = driver.execute_script(js_script)

            print(f"부품 가격 HTML: {part_price}")

            results.append(["혼다", part_model, "-", part_number_result, part_name_english, part_name_korean, part_price])
            print(["혼다", part_model, "-", part_number_result, part_name_english, part_name_korean, part_price])
        
        except TimeoutException:
            print(f"Timeout while retrieving results for part number: {part_number}")
            results.append(["혼다", "-", "-", part_number, "Timeout 발생", "", "", ""])
        except NoSuchElementException:
            print(f"No results found for part number: {part_number}")
            results.append(["혼다", "-", "-", part_number, "검색된 부품이 없습니다.", "", "", ""])
        except Exception as e:
            print(f"Error occurred while retrieving results for part number: {part_number}: {e}")
            results.append(["혼다", "-", "-", part_number, "에러 발생", "", "", ""])

    return results