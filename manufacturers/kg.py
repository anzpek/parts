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

def select_kg_model():
    model = None
    
    def set_model(selected_model):
        nonlocal model
        model = selected_model
        root.quit()

    root = Tk()
    root.title("모델 선택")
    root.attributes('-topmost', True)
    root.lift()

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)

    frame = ttk.Frame(root, padding="20")
    frame.pack(expand=True)

    model_options = ["G4 렉스턴", "렉스턴", "렉스턴 스포츠", "렉스턴(M&M)", "로디우스", "무쏘", "무쏘 스포츠", 
                     "뷰티풀 코란도", "액티언", "액티언 스포츠", "이스타나", "체어맨", "체어맨 W", 
                     "카이런", "코란도", "코란도 C", "코란도 스포츠", "코란도 이모션", "코란도 투리스모", 
                     "토레스", "토레스 EVX", "티볼리"]

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

def scrape_kg(driver, df, model):
    main_url = 'https://epc.kg-mobility.com/catalog/res3701i/groupInfo.do?schMode=popup&groupCd='
    wait = WebDriverWait(driver, 10)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"부품 번호 검색 중: {part_number}")

        try:
            driver.get(main_url)
        except Exception as e:
            print(f"메인 페이지를 여는 데 실패했습니다: {e}")
            continue
        
        try:
            part_list_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnPartListPopup > span')))
            part_list_button.click()
        except TimeoutException:
            print("부품 검색 창을 여는 데 실패했습니다.")
            continue
        
        try:
            driver.switch_to.window(driver.window_handles[-1])
        except Exception as e:
            print(f"새로운 창으로 전환하는 데 실패했습니다: {e}")
            continue
        
        try:
            # JavaScript를 사용하여 모델 선택
            js_script = f"""
            var select = document.querySelector('.nice-select[data-id="schMotorKind"]');
            select.click();
            var options = document.querySelectorAll('ul.selectList > li');
            options.forEach(function(option) {{
                if (option.innerText.trim() === "{model}") {{
                    option.click();
                }}
            }});
            """
            driver.execute_script(js_script)
        except Exception as e:
            print(f"JavaScript로 모델을 선택하는 데 실패했습니다: {e}")
            continue
        
        try:
            # JavaScript를 사용하여 부품 번호 입력
            js_script = f"""
            document.querySelector('#schPartNo').value = '{part_number}';
            """
            driver.execute_script(js_script)
        except Exception as e:
            print(f"JavaScript로 부품 번호를 입력하는 데 실패했습니다: {e}")
            continue
        
        try:
            # JavaScript를 사용하여 검색 버튼 클릭
            js_script = "document.querySelector('#btnSearch').click();"
            driver.execute_script(js_script)
        except Exception as e:
            print(f"JavaScript로 검색 버튼을 클릭하는 데 실패했습니다: {e}")
            continue
        
        try:
            search_result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#grid > div.tui-grid-content-area.tui-grid-show-lside-area > div.tui-grid-rside-area > div.tui-grid-body-area > div > div.tui-grid-table-container > table > tbody > tr')))
            search_result.click()
        except TimeoutException:
            print(f"검색 결과를 클릭하는 데 실패했습니다: {part_number}")
            continue

        try:
            # 검색 결과를 클릭하면 팝업이 닫히고 원래 창으로 돌아오므로, 원래 창으로 전환
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)  # 원래 창으로 전환 대기

            # 원래 창에서 결과 스크래핑
            js_script = """
            return {
                part_korean_name: document.querySelector('#pKnm').innerText,
                part_english_name: document.querySelector('#pEnm').innerText,
                part_price: document.querySelector('#prce2').innerText
            };
            """
            part_info = driver.execute_script(js_script)
            part_korean_name = part_info['part_korean_name']
            part_english_name = part_info['part_english_name']
            part_price = part_info['part_price']

            brand = "KG"
            year = "-"

            results.append([brand, year, model, part_english_name, part_number, part_korean_name, part_price])
            print([brand, year, model, part_english_name, part_number, part_korean_name, part_price])
        except TimeoutException:
            print(f"부품 정보를 스크래핑하는 데 실패했습니다: {part_number}")
            continue
        except NoSuchElementException as e:
            print(f"필수 요소를 찾는 데 실패했습니다: {e}")
            continue

    return results
