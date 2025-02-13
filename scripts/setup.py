import os
import subprocess
from datetime import datetime, timedelta

# ✅ 필수 환경변수 입력 함수
def get_required_input(prompt):
    """사용자가 필수 입력값을 입력할 때까지 반복 요청"""
    while True:
        value = input(f"{prompt}: ").strip()
        if value:
            return value
        print("⚠️ 이 값은 반드시 입력해야 합니다.")

# ✅ `SEAT_CLASS` 검증 함수
def get_valid_seat_class():
    """사용자가 올바른 좌석 등급을 입력할 때까지 반복 요청"""
    valid_seat_classes = ["일반실", "특실/우등실", "유아", "자유석/입석"]
    while True:
        value = input(f"💺 좌석 등급을 입력하세요 ({', '.join(valid_seat_classes)} 중 하나): ").strip() or '일반실'
        if value in valid_seat_classes:
            return value
        print(f"⚠️ 잘못된 입력입니다. 다음 중 하나를 입력하세요: {', '.join(valid_seat_classes)}")

# ✅ `SEAT_CLASS` 검증 함수
def get_valid_seat_type():
    """사용자가 올바른 좌석 타입을 입력할 때까지 반복 요청"""
    valid_seat_types = ["기본", "1인석", "창측좌석", "내측좌석"]
    while True:
        value = input(f"💺 좌석 타입을 입력하세요 ({', '.join(valid_seat_types)} 중 하나): ").strip() or '기본'
        if value in valid_seat_types:
            return value
        print(f"⚠️ 잘못된 입력입니다. 다음 중 하나를 입력하세요: {', '.join(valid_seat_types)}")

# ✅ `SEAT_CLASS` 검증 함수
def get_valid_seat_direction():
    """사용자가 올바른 좌석 방향을 입력할 때까지 반복 요청"""
    valid_seat_directions = ["좌석방향", "순방향석", "역방향석"]
    while True:
        value = input(f"💺 좌석 방향을 입력하세요 ({', '.join(valid_seat_directions)} 중 하나): ").strip() or '좌석방향'
        if value in valid_seat_directions:
            return value
        print(f"⚠️ 잘못된 입력입니다. 다음 중 하나를 입력하세요: {', '.join(valid_seat_directions)}")

# ✅ `SEAT_CLASS` 검증 함수
def get_valid_seat_discount_type():
    """사용자가 올바른 좌석 할인 유형을 입력할 때까지 반복 요청"""
    valid_seat_discount_types = ["기본", "유아동반", "편한대화", "수동휠체어석", "전동휠체어석", "수유실 인접", "자전거거치대"]
    while True:
        value = input(f"💺 좌석 할인 유형을 입력하세요 ({', '.join(valid_seat_discount_types)} 중 하나): ").strip() or '기본'
        if value in valid_seat_discount_types:
            return value
        print(f"⚠️ 잘못된 입력입니다. 다음 중 하나를 입력하세요: {', '.join(valid_seat_discount_types)}")

# ✅ 날짜 및 시간 검증 함수
def get_valid_datetime():
    """사용자가 현재 날짜 및 시간보다 크거나 같은 값만 입력하도록 검증"""
    now = datetime.now()
    min_departure_time = now + timedelta(minutes=21)  # 현재 시간보다 21분 이후

    while True:
        month = int(input(f"📅 탑승할 월을 입력하세요 (현재 월: {now.month} 이상): ").strip() or now.month)
        if month < now.month:
            print("⚠️ 탑승할 월은 현재 월보다 작을 수 없습니다.")
            continue

        day = int(input(f"📆 탑승할 일을 입력하세요 (현재 일: {now.day} 이상): ").strip() or now.day)
        if month == now.month and day < now.day:
            print("⚠️ 탑승할 일은 현재 날짜보다 작을 수 없습니다.")
            continue

        # ✅ 내일 이후면 시간 제한 없이 입력 가능
        if (month, day) > (now.month, now.day):
            hour = int(input("⏰ 탑승할 시간을 입력하세요: ").strip() or '0')
            minute = int(input("⏳ 탑승할 분을 입력하세요: ").strip() or '0')
            return month, day, hour, minute

        # ✅ 오늘 날짜라면 현재 시간보다 크거나 같은 시간 입력 필요
        while True:
            hour = int(input(f"⏰ 탑승할 시간을 입력하세요 (현재 시간: {min_departure_time.hour} 이상): ").strip() or min_departure_time.hour)
            if hour < now.hour:
                print("⚠️ 탑승할 시간은 현재 시간보다 작을 수 없습니다.")
                continue

            minute = int(input(f"⏳ 탑승할 분을 입력하세요 (현재 분: {min_departure_time.minute} 이상): ").strip() or min_departure_time.minute)
            if hour == now.hour and minute < now.minute + 20:
                print("⚠️ 출발 시간은 현재 시간보다 최소 20분 이후여야 합니다.")
                continue

            return month, day, hour, minute

# ✅ 사용자 입력을 받아 환경변수 업데이트하는 함수
def update_env():
    env_variables = {
        "MEMBERSHIP_NUMBER": "🔑 멤버십 번호를 입력하세요",
        "PASSWORD": "🔒 비밀번호를 입력하세요",
        "START_STATION": "🚉 출발역을 입력하세요",
        "END_STATION": "🏁 도착역을 입력하세요",
        "MAX_RETRIES": "🔄 최대 조회 시도 횟수를 입력하세요 (예: 10)"
    }

    new_env_data = []
    print("\n🔧 환경변수를 설정합니다. `MEMBERSHIP_NUMBER`와 `PASSWORD`는 반드시 입력해야 합니다.\n")

    for key, prompt in env_variables.items():
        if key in ["MEMBERSHIP_NUMBER", "PASSWORD"]:
            # 필수 입력값 (반드시 입력할 때까지 반복)
            value = get_required_input(prompt)
        else:
            # 선택 입력값 (입력하지 않으면 기존 값 유지)
            value = input(f"{prompt} [{os.getenv(key, '')}]: ").strip()
            if value == '':
                if key == 'START_STATION': value = '서울'
                elif key == 'END_STATION': value = '부산'
                elif key == 'MAX_RETRIES': value = '5'

        new_env_data.append(f"{key}={value}")

    # ✅ `SEAT_CLASS` 입력 (검증된 값만 허용)
    seat_class = get_valid_seat_class()
    new_env_data.append(f"SEAT_CLASS={seat_class}")

    # ✅ `SEAT_TYPE` 입력 (검증된 값만 허용)
    seat_type = get_valid_seat_type()
    new_env_data.append(f"SEAT_TYPE={seat_type}")

    # ✅ `SEAT_DIRECTION` 입력 (검증된 값만 허용)
    seat_dir = get_valid_seat_direction()
    new_env_data.append(f"SEAT_DIRECTION={seat_dir}")

    # ✅ `SEAT_DISCOUNT` 입력 (검증된 값만 허용)
    seat_dsct = get_valid_seat_discount_type()
    new_env_data.append(f"SEAT_DISCOUNT={seat_dsct}")

    

    # ✅ `MONTH`, `DAY`, `HOUR`, `MINUTE` 검증 (현재 시간보다 크거나 같아야 함)
    month, day, hour, minute = get_valid_datetime()
    new_env_data.append(f"MONTH={month:02}")
    new_env_data.append(f"DAY={day:02}")
    new_env_data.append(f"HOUR={hour:02}")
    new_env_data.append(f"MINUTE={minute:02}")

    # ✅ 입력된 값을 .env 파일로 저장
    with open(".env", "w", encoding="utf-8") as env_file:
        env_file.write("\n".join(new_env_data) + "\n")
    
    print("\n✅ 환경변수가 업데이트되었습니다.\n")

# ✅ `requirements.txt` 내 패키지를 설치하는 함수
def install_requirements():
    """requirements.txt 기반으로 패키지 설치"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 프로젝트 루트 경로
    requirements_path = os.path.join(base_dir, "requirements.txt")

    if not os.path.exists(requirements_path):
        print(f"❌ ERROR: requirements.txt 파일을 찾을 수 없습니다: {requirements_path}")
        return

    print(f"\n📦 requirements.txt 경로: {requirements_path}\n")
    subprocess.run(["pip", "install", "-r", requirements_path], check=True)
    print("\n✅ 패키지 설치가 완료되었습니다.\n")

# ✅ `korail_macro.py` 실행
def run_macro():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 프로젝트 루트 경로
    macro_path = os.path.join(base_dir, "src/korail_macro.py")

    if not os.path.exists(macro_path):
        print(f"❌ ERROR: korail_macro.py 파일을 찾을 수 없습니다: {macro_path}")
        return

    print("\n🚀 `korail_macro.py`를 실행합니다...\n")
    subprocess.run(["python", macro_path], check=True)

if __name__ == "__main__":
    update_env()           # 1️⃣ 환경변수 설정
    install_requirements() # 2️⃣ 패키지 설치
    run_macro()            # 3️⃣ `korail_macro.py` 실행