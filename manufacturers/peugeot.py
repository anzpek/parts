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

def scrape_peugeot(driver, df):
    url = 'https://base.epeugeot.co.kr/price'
    wait = WebDriverWait(driver, 20)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)
        
        # 검색 유형 선택: 품번
        try:
            js_script = """
            document.querySelector('#SrhCol').value = 'PartNumber';
            var event = new Event('change');
            document.querySelector('#SrhCol').dispatchEvent(event);
            """
            driver.execute_script(js_script)
            print("검색 유형 선택 완료: 품번")
        except Exception as e:
            print(f"JavaScript로 검색 유형을 선택하는 데 실패했습니다: {e}")
            results.append(["푸조", "-", "-", part_number, "검색 유형 선택 실패", "", "", ""])
            continue

        # 부품 번호 입력
        try:
            js_script = f"""
            document.querySelector('#SrhWord').value = '{part_number}';
            """
            driver.execute_script(js_script)
            print(f"부품 번호 입력 완료: {part_number}")
        except Exception as e:
            print(f"JavaScript로 부품 번호를 입력하는 데 실패했습니다: {e}")
            results.append(["푸조", "-", "-", part_number, "부품 번호 입력 실패", "", "", ""])
            continue

        # 검색 버튼 클릭
        try:
            js_script = """
            document.querySelector('#searchform > div > input[type=submit]:nth-child(4)').click();
            """
            driver.execute_script(js_script)
            print(f"검색 버튼 클릭 완료: {part_number}")
        except Exception as e:
            print(f"JavaScript로 검색 버튼을 클릭하는 데 실패했습니다: {e}")
            results.append(["푸조", "-", "-", part_number, "검색 버튼 클릭 실패", "", "", ""])
            continue

        # 검색 결과 가져오기
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.importer-wrap > section > div.price-wrap > div.price-tb-mask > table > tbody > tr:nth-child(2)')))
            
            # 모델명
            try:
                part_model = driver.find_element(By.CSS_SELECTOR, 'body > div.importer-wrap > section > div.price-wrap > div.price-tb-mask > table > tbody > tr:nth-child(2) > td:nth-child(2)').text.strip()
            except NoSuchElementException:
                part_model = ""
            print(f"모델명 가져오기 완료: {part_model}")
            
            # 부품번호
            part_number_result = driver.find_element(By.CSS_SELECTOR, 'body > div.importer-wrap > section > div.price-wrap > div.price-tb-mask > table > tbody > tr:nth-child(2) > td:nth-child(3)').text.strip()
            print(f"부품번호 가져오기 완료: {part_number_result}")
            
            # 부품명 (영문)
            part_name_english = driver.find_element(By.CSS_SELECTOR, 'body > div.importer-wrap > section > div.price-wrap > div.price-tb-mask > table > tbody > tr:nth-child(2) > td:nth-child(4)').text.strip()
            print(f"부품명(영문) 가져오기 완료: {part_name_english}")
            
            # 부품명 (한글)
            part_name_korean = driver.find_element(By.CSS_SELECTOR, 'body > div.importer-wrap > section > div.price-wrap > div.price-tb-mask > table > tbody > tr:nth-child(2) > td:nth-child(5)').text.strip()
            print(f"부품명(한글) 가져오기 완료: {part_name_korean}")
            
            # 부품 가격
            part_price = driver.find_element(By.CSS_SELECTOR, 'body > div.importer-wrap > section > div.price-wrap > div.price-tb-mask > table > tbody > tr:nth-child(2) > td:nth-child(6)').text.strip()
            print(f"부품 가격 가져오기 완료: {part_price}")

            results.append(["푸조", "-", part_model, part_number_result, part_name_english, part_name_korean, part_price])
            print(["푸조", "-", part_model, part_number_result, part_name_english, part_name_korean, part_price])
        
        except TimeoutException:
            print(f"Timeout while retrieving results for part number: {part_number}")
            results.append(["푸조", "-", "-", part_number, "Timeout 발생", "", "", ""])
        except NoSuchElementException:
            print(f"No results found for part number: {part_number}")
            results.append(["푸조", "-", "-", part_number, "검색된 부품이 없습니다.", "", "", ""])
        except Exception as e:
            print(f"Error occurred while retrieving results for part number: {part_number}: {e}")
            results.append(["푸조", "-", "-", part_number, "에러 발생", "", "", ""])

    return results