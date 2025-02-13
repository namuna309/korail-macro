import os
from korail_login import KorailLogin
from korail_search import KorailSearch
from korail_utils import get_korail_date
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(override=True)

if __name__ == "__main__":
    # 설정값 입력
    start_station = os.getenv('START_STATION')
    end_station = os.getenv('END_STATION')
    month = int(os.getenv('MONTH'))
    day = int(os.getenv('DAY'))
    hour = int(os.getenv('HOUR'))
    minute = int(os.getenv('MINUTE'))
    seat_class = os.getenv('SEAT_CLASS')
    max_retries = os.getenv('MAX_RETRIES')
    seat_type = os.getenv('SEAT_TYPE')
    seat_direction = os.getenv('SEAT_DIRECTION')
    seat_discount = os.getenv('SEAT_DISCOUNT')


    # 날짜 변환
    year, month1, month2, day1, day2, weekday = get_korail_date(month, day)

    # 로그인 실행
    login = KorailLogin()
    driver = login.login()

    # 날짜 및 조회 실행
    search = KorailSearch(driver, start_station, end_station, year, month1, month2, day1, day2, weekday, hour, minute, seat_class, max_retries, seat_type, seat_direction, seat_discount)
    search.go_reservation_page()
    search.select_options()
    search.select_date()
    search.search_ticket()

