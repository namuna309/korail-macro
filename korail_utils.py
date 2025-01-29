import datetime

def get_korail_date(month: int, day: int):
    """현재 연도 및 해당 날짜의 요일 반환"""
    current_year = datetime.datetime.now().year
    target_date = datetime.date(current_year, month, day)
    weekday_map = ['월', '화', '수', '목', '금', '토', '일']
    weekday = weekday_map[target_date.weekday()]
    return str(current_year), f"{month:02}", f"{month}", f"{day:02}", f"{day}", weekday
