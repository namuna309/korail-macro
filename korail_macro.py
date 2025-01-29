import os
from datetime import date, datetime
from korail_login import KorailLogin
from korail_search import KorailSearch
from korail_utils import get_korail_date
from dotenv import load_dotenv

if __name__ == "__main__":
    # 설정값 입력
    start_station = os.getenv('START_STATION') or '서울'
    end_station = os.getenv('END_STATION') or '부산'
    month = int(os.getenv('MONTH') or date.today().month)
    day = int(os.getenv('DAY') or date.today().day)
    hour = int(os.getenv('HOUR') or datetime.now().hour)
    minute = int(os.getenv('MINUTE') or datetime.now().minute)
    seat_type = os.getenv('SEAT_TYPE') or '일반실'
    max_retries = os.getenv('MAX_RETRIES') or '5'

    # 날짜 변환
    year, month1, month2, day1, day2, weekday = get_korail_date(month, day)

    # 로그인 실행
    login = KorailLogin()
    driver = login.login()

    # 날짜 및 조회 실행
    search = KorailSearch(driver, start_station, end_station, year, month1, month2, day1, day2, weekday, hour, minute, seat_type, max_retries)
    search.select_date()
    search.search_ticket()

