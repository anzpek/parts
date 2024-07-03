import tkinter as tk
from tkinter import ttk
from tkinter.tix import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from PIL import Image
from io import BytesIO

def select_jeep_model():
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

    model_options = [
        "Renegade", "Cherokee", "Commander", "Compass", "New Compass",
        "Grand Cherokee", "Grand Cherokee (구)", "Wrangler", "Wrangler 4xe",
        "New Wrangler", "Gladiator", "All-New Grand Cherokee L"
    ]

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

def scrape_jeep(driver, df, model):
    url = 'https://www.jeep.co.kr/parts.html'
    wait = WebDriverWait(driver, 20)
    results = []

    for index, row in df.iterrows():
        part_number = str(row[df.columns[0]]).strip()
        print(f"Searching for part number: {part_number}")

        driver.get(url)
        
        # 페이지가 완전히 로드되도록 충분한 시간 대기
        time.sleep(5)  # 로드 시간을 충분히 주기 위해 5초 대기
        print("페이지 로드 대기 완료")

        # 스크린샷을 메모리에 저장
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))

        # (이미지를 처리하는 코드를 여기에 추가할 수 있습니다.)
        
        # 모델 선택
        try:
            model_selector = driver.execute_script("return document.querySelector('#car_models');")
            if model_selector is None:
                print("모델 선택 요소가 존재하지 않습니다.")
                results.append(["지프", "-", model, part_number, "모델 선택 요소 없음", "", "", ""])
                continue
            print(f"모델 선택 요소 찾기 성공: {model_selector}")

            js_script = f"""
            var select = document.querySelector('#car_models');
            if (select) {{
                select.value = '{model}';
                var event = new Event('change');
                select.dispatchEvent(event);
            }} else {{
                throw new Error('모델 선택 요소를 찾을 수 없습니다.');
            }}
            """
            driver.execute_script(js_script)
            print(f"모델 선택 완료: {model}")
        except Exception as e:
            print(f"JavaScript로 모델을 선택하는 데 실패했습니다: {e}")
            results.append(["지프", "-", model, part_number, "모델 선택 실패", "", "", ""])
            continue

        # 부품 번호 입력
        try:
            part_number_input = driver.execute_script("return document.querySelector('#part_number');")
            if part_number_input is None:
                print("부품 번호 입력 요소가 존재하지 않습니다.")
                results.append(["지프", "-", model, part_number, "부품 번호 입력 요소 없음", "", "", ""])
                continue
            print(f"부품 번호 입력 요소 찾기 성공: {part_number_input}")

            js_script = f"""
            var partNumberInput = document.querySelector('#part_number');
            if (partNumberInput) {{
                partNumberInput.value = '{part_number}';
            }} else {{
                throw new Error('부품 번호 입력 요소를 찾을 수 없습니다.');
            }}
            """
            driver.execute_script(js_script)
            print(f"부품 번호 입력 완료: {part_number}")
        except Exception as e:
            print(f"JavaScript로 부품 번호를 입력하는 데 실패했습니다: {e}")
            results.append(["지프", "-", model, part_number, "부품 번호 입력 실패", "", "", ""])
            continue

        # 검색 버튼 클릭
        try:
            search_button = driver.execute_script("return document.querySelector('a.cta[data-lid=\"parts_search_button\"]');")
            if search_button is None:
                print("검색 버튼이 존재하지 않습니다.")
                results.append(["지프", "-", model, part_number, "검색 버튼 없음", "", "", ""])
                continue
            print(f"검색 버튼 찾기 성공: {search_button}")

            js_script = """
            var searchButton = document.querySelector('a.cta[data-lid="parts_search_button"]');
            if (searchButton) {
                searchButton.click();
            } else {
                throw new Error('검색 버튼을 찾을 수 없습니다.');
            }
            """
            driver.execute_script(js_script)
            print(f"검색 버튼 클릭 완료: {part_number}")
        except Exception as e:
            print(f"JavaScript로 검색 버튼을 클릭하는 데 실패했습니다: {e}")
            results.append(["지프", "-", model, part_number, "검색 버튼 클릭 실패", "", "", ""])
            continue

        # 검색 결과 가져오기
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#info > table > tbody > tr:nth-child(2) > td:nth-child(1)")))
            print("검색 결과 대기 완료")
            
            part_model = driver.find_element(By.CSS_SELECTOR, "#info > table > tbody > tr:nth-child(2) > td:nth-child(1)").text.strip()
            part_number_result = driver.find_element(By.CSS_SELECTOR, "#info > table > tbody > tr:nth-child(2) > td:nth-child(2)").text.strip()
            part_name_english = driver.find_element(By.CSS_SELECTOR, "#info > table > tbody > tr:nth-child(2) > td:nth-child(3)").text.strip()
            part_name_korean = driver.find_element(By.CSS_SELECTOR, "#info > table > tbody > tr:nth-child(2) > td:nth-child(4)").text.strip()
            part_price = driver.find_element(By.CSS_SELECTOR, "#info > table > tbody > tr:nth-child(2) > td:nth-child(5)").text.strip()

            results.append(["지프", part_model, model, part_number_result, part_name_english, part_name_korean, part_price])
            print(["지프", part_model, model, part_number_result, part_name_english, part_name_korean, part_price])
        
        except TimeoutException:
            print(f"Timeout while retrieving results for part number: {part_number}")
            results.append(["지프", "-", model, part_number, "Timeout 발생", "", "", ""])
        except NoSuchElementException:
            print(f"No results found for part number: {part_number}")
            results.append(["지프", "-", model, part_number, "검색된 부품이 없습니다.", "", "", ""])
        except Exception as e:
            print(f"Error occurred while retrieving results for part number: {part_number}: {e}")
            results.append(["지프", "-", model, part_number, "에러 발생", "", "", ""])

        # 메모리에서 이미지 삭제
        del image

    return results