import time
import datetime
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class KorailSearch:
    def __init__(self, driver, start, end, year, month1, month2, day1, day2, weekday, hour, minute, seat_class, max_retries, seat_type, seat_direction, seat_discount):
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
        self.seat_class = seat_class
        self.max_retries = int(max_retries)
        self.seat_type = seat_type
        self.seat_direction = seat_direction
        self.seat_discount = seat_discount

    def go_reservation_page(self):
        try:
            self.driver.get('https://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li/a[contains(@onclick, 'm_prd_mypage_main_link')]")))
            print("✅ 승차권 예매 페이지 이동 완료")
        except Exception as e:
            print(f'⚠️ 승차권 예매 페이지 이동 중 에러 발생: {e}')

    def select_options(self):
        """좌석 종류, 방향, 할인 좌석 선택"""
        type_dict = { '기본': '000', '1인석': '011', '창측좌석': '012', '내측좌석': '013' }
        dir_dict = { '좌석방향': '000', '순방향석': '009', '역방향석': '010' }
        dsct_dict = { '기본': '015', '유아동반': '015', '편한대화': '019', '수동휠체어석': '021', '전동휠체어석': '028', '수유실 인접': 'XXX', '자전거거치대': '032' }  # 2층석, 노트북석 선택 불가
        try:
            # 좌석 종류 선택
            select_type = Select(self.driver.find_element(By.ID, "seat01"))
            select_type.select_by_value(type_dict[self.seat_type])

            # 좌석 방향 선택
            select_dir = Select(self.driver.find_element(By.ID, "seat02"))
            select_dir.select_by_value(dir_dict[self.seat_direction])

            # 추가 사항 선택
            select_discount = Select(self.driver.find_element(By.ID, "seat03"))
            select_discount.select_by_value(dsct_dict[self.seat_discount])
        except Exception as e:
            print(f"⚠️ 좌석 종류 선택 중 오류 발생: {e}")


    def select_date(self):
        """출발역, 도착역 및 날짜 선택"""
        try:
            # 출발역 입력
            go_start = self.driver.find_element(By.NAME, "txtGoStart")
            go_start.clear()
            go_start.send_keys(self.start)

            # 도착역 입력
            go_end = self.driver.find_element(By.NAME, "txtGoEnd")
            go_end.clear()
            go_end.send_keys(self.end)

            # 출발년도 선택
            go_year = Select(self.driver.find_element(By.NAME, "selGoYear"))
            go_year.select_by_value(self.year)

            # 출발월 선택
            go_month = Select(self.driver.find_element(By.NAME, "selGoMonth"))
            go_month.select_by_value(self.month1)

            # 출발일 선택 
            go_day = Select(self.driver.find_element(By.NAME, "selGoDay"))
            go_day.select_by_value(self.day1)
            
            # 출발시 선택
            go_hour = Select(self.driver.find_element(By.NAME, "selGoHour"))
            go_hour.select_by_value(str(self.hour))

            ktx_srt_radio = self.driver.find_element(By.XPATH, "//*[@id=\"selGoTrainRa00\"]")
            ktx_srt_radio.click()

        except Exception as e:
            print(f"⚠️ 날짜 선택 중 오류 발생: {e}")

    def search_ticket(self):
        """예매 가능한 좌석 찾기 (가장 가까운 기차 포함)"""
        try:
            self.driver.find_element(By.XPATH, '//img[@alt="조회하기"]').click()
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tbl_h")))

            for attempt in range(self.max_retries):
                print(f"🔄 {attempt + 1}번째 조회 시도...")

                rows = self.driver.find_elements(By.XPATH, "//table[contains(@class, 'tbl_h')]//tbody/tr")
                available_times = []  # 예약 가능한 모든 출발 시간 저장

                for row in rows:
                    rail_type = row.find_element(By.XPATH, "./td[2]").get_attribute('title').strip()
                    if rail_type == 'KTX':
                        departure_time = row.find_element(By.XPATH, "./td[3]").text.strip()
                        
                        # 출발역 정보 제거 (예: '서울\n22:28' → '22:28')
                        departure_time = departure_time.split("\n")[-1].strip()

                        # 예약 가능한 모든 기차 시간 저장
                        available_times.append(departure_time)

                        # 원하는 시간과 정확히 일치하는 기차 찾기
                        if departure_time == f"{self.hour}:{self.minute:02}":
                            print(f"⏰ {departure_time} 기차 찾음!")
                            if self.reserve_seat(row): return
                    else:
                        continue

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
                            if self.reserve_seat(row): return
                            

                # 원하는 시간도, 가장 가까운 시간도 없으면 재조회
                self.retry_search()
            print('좌석 예약 실패\n')
        except Exception as e:
            print(f"⚠️ 조회 중 오류 발생: {e}")

    def reserve_seat(self, row):
        """좌석 예약하기"""
        try:
            general_seat = row.find_element(By.XPATH, "./td[6]//img")
            seat_status = general_seat.get_attribute("alt")

            seat_types = {"특실/우등실": 5, "일반실": 6, "유아": 7, "자유석/입석": 8}
            seat_colunm = seat_types[self.seat_class]

            seat_img = row.find_element(By.XPATH, f"./td[{seat_colunm}]//img")
            alt_text = seat_img.get_attribute("alt")
            
            if alt_text == "예약하기": 
                seat_img.click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li/a[contains(@onclick, 'm_prd_mypage_main_link')]")))
                print("🎉 예매 성공!")
                return True
            else:
                print("⚠️ 좌석이 매진됨.")
                return False

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
        future_times = {t: v for t, v in time_diffs.items() if t > target_time}
        if future_times:
            return future_times[min(future_times.keys())]

        # 이후 시간이 없으면 이전 시간 중 가장 가까운 기차 찾기
        past_times = {t: v for t, v in time_diffs.items() if t < target_time}
        if past_times:
            return past_times[max(past_times.keys())]

        return None  # 이용 가능한 기차가 없음

