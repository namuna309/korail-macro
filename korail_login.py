import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class KorailLogin:
    def __init__(self):
        self.membership_number = os.getenv('MEMBERSHIP_NUMBER', '맴버십번호를 입력해주세요')
        self.password = os.getenv('PASSWORD', '패스워드를 입력해주세요')

    def login(self):
        """코레일 로그인"""
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)  # 브라우저가 자동으로 닫히지 않도록 설정
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://www.letskorail.com/korail/com/login.do")

        try:
            # 로그인 정보 입력
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtMember"))).send_keys(self.membership_number)
            driver.find_element(By.ID, "txtPwd").send_keys(self.password)
            driver.find_element(By.XPATH, "//li[@class='btn_login']/a").click()

            # 로그인 성공 확인
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li/a[contains(@onclick, 'm_prd_mypage_main_link')]")))

            print("✅ 로그인 성공!")
            self.close_popups(driver)

            return driver

        except Exception as e:
            print(f"⚠️ 로그인 중 오류 발생: {e}")
            driver.quit()

    @staticmethod
    def close_popups(driver):
        """로그인 후 자동 팝업창 닫기"""
        try:
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            main_window = driver.current_window_handle

            for window in driver.window_handles:
                if window != main_window:
                    driver.switch_to.window(window)
                    driver.close()

            driver.switch_to.window(main_window)
            print("✅ 모든 팝업창 닫기 완료!")

        except Exception as e:
            print(f"⚠️ 팝업창 닫기 중 오류 발생: {e}")
