import time
import datetime
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class KorailSearch:
    def __init__(self, driver, start, end, year, month1, month2, day1, day2, weekday, hour, minute, seat_type, max_retries):
        self.driver = driver
        self.start = start
        self.end = end
        self.year = year
        self.month1 = month1
        self.month2 = month2
        self.day1 = day1
        self.day2 = day2
        self.weekday = weekday
        self.hour = hour
        self.minute = minute
        self.seat_type = seat_type
        self.max_retries = int(max_retries)

    def select_date(self):
        """출발역, 도착역 및 날짜 선택"""
        try:
            # 출발역 입력
            go_start = self.driver.find_element(By.ID, "txtGoStart")
            go_start.clear()
            go_start.send_keys(self.start)

            # 도착역 입력
            go_end = self.driver.find_element(By.ID, "txtGoEnd")
            go_end.clear()
            go_end.send_keys(self.end)

            # 날짜 선택 버튼 클릭
            self.driver.find_element(By.XPATH, '//img[@alt="달력"]').click()
            WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))

            # 팝업창 전환 및 날짜 선택
            main_window = self.driver.current_window_handle
            popup_window = [w for w in self.driver.window_handles if w != main_window][0]
            self.driver.switch_to.window(popup_window)

            # 팝업창이 완전히 로드될 때까지 대기
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            date_xpath = f"//a[@href=\"javascript:putDate('{self.year}','{self.month1}','{self.month2}','{self.day1}','{self.day2}','{self.weekday}')\"]"
            
            # 원하는 날짜가 있는지 먼저 확인 후 클릭
            date_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, date_xpath))
            )

            # 클릭 가능할 때까지 대기 후 클릭
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, date_xpath))).click()
            print("✅ 날짜 클릭 완료")
            self.driver.switch_to.window(main_window)

            # 시간 선택
            Select(self.driver.find_element(By.ID, "time")).select_by_value(f"{self.hour}")

        except Exception as e:
            print(f"⚠️ 날짜 선택 중 오류 발생: {e}")

    def search_ticket(self):
        """예매 가능한 좌석 찾기 (가장 가까운 기차 포함)"""
        try:
            self.driver.find_element(By.XPATH, '//img[@alt="승차권예매"]').click()
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tbl_h")))

            for attempt in range(self.max_retries):
                print(f"🔄 {attempt + 1}번째 조회 시도...")

                rows = self.driver.find_elements(By.XPATH, "//table[contains(@class, 'tbl_h')]//tbody/tr")
                available_times = []  # 예약 가능한 모든 출발 시간 저장

                for row in rows:
                    departure_time = row.find_element(By.XPATH, "./td[3]").text.strip()
                    
                    # 출발역 정보 제거 (예: '서울\n22:28' → '22:28')
                    departure_time = departure_time.split("\n")[-1].strip()
                    
                    print(f"🔍 조회된 출발 시간: {departure_time}")  # 디버깅 코드

                    # 예약 가능한 모든 기차 시간 저장
                    available_times.append(departure_time)

                    # 원하는 시간과 정확히 일치하는 기차 찾기
                    if departure_time == f"{self.hour}:{self.minute:02}":
                        print(f"⏰ {departure_time} 기차 찾음!")
                        self.reserve_seat(row)
                        return

                # 원하는 기차 시간이 없으면 가장 가까운 시간 찾기
                print(f"🧐 사용 가능한 출발 시간 목록: {available_times}")  # 디버깅 코드
                closest_time = self.find_closest_time(available_times, self.hour, self.minute)
                print(f"🧐 가장 가까운 기차 시간: {closest_time}")  # 디버깅 코드

                if closest_time:
                    print(f"🔍 원하는 시간의 기차가 없음. 가장 가까운 시간({closest_time}) 기차를 조회합니다.")
                    for row in rows:
                        departure_time = row.find_element(By.XPATH, "./td[3]").text.strip()
                        departure_time = departure_time.split("\n")[-1].strip()
                        if departure_time == closest_time:
                            print('예매를 시도합니다')
                            self.reserve_seat(row)
                            return

                # 원하는 시간도, 가장 가까운 시간도 없으면 재조회
                self.retry_search()

        except Exception as e:
            print(f"⚠️ 조회 중 오류 발생: {e}")

    def reserve_seat(self, row):
        """좌석 예약하기"""
        try:
            general_seat = row.find_element(By.XPATH, "./td[6]//img")
            seat_status = general_seat.get_attribute("alt")

            seat_types = {"특실/우등실": 5, "일반실": 6, "유아": 7, "자유석/입석": 8}
            seat_colunm = seat_types[self.seat_type]

            seat_img = row.find_element(By.XPATH, f"./td[{seat_colunm}]//img")
            alt_text = seat_img.get_attribute("alt")
            
            if alt_text == "예약하기": 
                seat_img.click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li/a[contains(@onclick, 'm_prd_mypage_main_link')]")))
                print("🎉 예매 성공!")
            else:
                print("⚠️ 좌석이 매진됨. 다음 기차 확인.")

        except Exception as e:
            print(f"⚠️ 예매 시 오류 발생: {e}")

    def retry_search(self):
        """조회하기 버튼 클릭 후 랜덤 대기"""
        try:
            self.driver.find_element(By.XPATH, "//img[@alt='조회하기']").click()
            wait_time = random.uniform(1, 3)
            print(f"⏳ 랜덤 대기 {wait_time:.2f}초 후 재조회...")
            time.sleep(wait_time)

        except Exception as e:
            print(f"⚠️ 조회 버튼 클릭 실패: {e}")

    @staticmethod
    def find_closest_time(available_times, target_hour, target_minute):
        """가장 가까운 기차 시간 찾기"""
        now = datetime.datetime.now()
        now_minutes = now.hour * 60 + now.minute  # 현재 시간을 분 단위로 변환
        target_time = int(target_hour) * 60 + int(target_minute)  # 목표 시간 분 단위 변환
        time_diffs = {}

        for time_str in available_times:
            try:
                time_str = time_str.strip()  # 문자열 공백 제거
                hour, minute = map(int, time_str.split(":"))  # 시/분을 정수로 변환
                train_time = hour * 60 + minute  # 분 단위 변환

                # 현재 시간보다 20분 이내이면 예약 제외
                if train_time - now_minutes < 20:
                    print(f"⚠️ 출발 시간 {time_str}은 현재 시간과 20분 이내로 예약 불가")
                    continue

                time_diffs[train_time] = time_str
            except ValueError:
                print(f"⚠️ 잘못된 시간 형식 무시: {time_str}")
                continue  # 예외 발생 시 무시하고 다음 값 처리

        # 현재 시간 이후의 가장 가까운 기차 찾기
        future_times = {t: v for t, v in time_diffs.items() if t >= target_time}
        if future_times:
            return future_times[min(future_times.keys())]

        # 이후 시간이 없으면 이전 시간 중 가장 가까운 기차 찾기
        past_times = {t: v for t, v in time_diffs.items() if t < target_time}
        if past_times:
            return past_times[max(past_times.keys())]

        return None  # 이용 가능한 기차가 없음

