import os
import subprocess
from datetime import datetime

# ✅ 필수 환경변수 입력 함수
def get_required_input(prompt):
    """사용자가 필수 입력값을 입력할 때까지 반복 요청"""
    while True:
        value = input(f"{prompt}: ").strip()
        if value:
            return value
        print("⚠️ 이 값은 반드시 입력해야 합니다.")

# ✅ `SEAT_TYPE` 검증 함수
def get_valid_seat_type():
    """사용자가 올바른 좌석 타입을 입력할 때까지 반복 요청"""
    valid_seat_types = ["일반실", "특실/우등실", "유아", "자유석/입석"]
    while True:
        value = input(f"💺 좌석 타입을 입력하세요 ({', '.join(valid_seat_types)} 중 하나): ").strip()
        if value in valid_seat_types:
            return value
        print(f"⚠️ 잘못된 입력입니다. 다음 중 하나를 입력하세요: {', '.join(valid_seat_types)}")

# ✅ 날짜 및 시간 검증 함수
def get_valid_datetime():
    """사용자가 현재 날짜 및 시간보다 크거나 같은 값만 입력하도록 검증"""
    now = datetime.now()

    while True:
        month = int(input(f"📅 탑승할 월을 입력하세요 (현재 월: {now.month} 이상): ").strip() or now.month)
        if month < now.month:
            print("⚠️ 탑승할 월은 현재 월보다 작을 수 없습니다.")
            continue

        day = int(input(f"📆 탑승할 일을 입력하세요 (현재 일: {now.day} 이상): ").strip() or now.day)
        if month == now.month and day < now.day:
            print("⚠️ 탑승할 일은 현재 날짜보다 작을 수 없습니다.")
            continue

        hour = int(input(f"⏰ 탑승할 시간을 입력하세요 (현재 시간: {now.hour} 이상): ").strip() or now.hour)
        if month == now.month and day == now.day and hour < now.hour:
            print("⚠️ 탑승할 시간은 현재 시간보다 작을 수 없습니다.")
            continue

        minute = int(input(f"⏳ 탑승할 분을 입력하세요 (현재 분: {now.minute} 이상): ").strip() or now.minute)
        if month == now.month and day == now.day and hour == now.hour and minute < now.minute:
            print("⚠️ 탑승할 분은 현재 분보다 작을 수 없습니다.")
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
            value = input(f"{prompt} [{os.getenv(key, '')}]: ").strip() or os.getenv(key, "")

        new_env_data.append(f"{key}={value}")

    # ✅ `SEAT_TYPE` 입력 (검증된 값만 허용)
    seat_type = get_valid_seat_type()
    new_env_data.append(f"SEAT_TYPE={seat_type}")

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
    print("\n📦 `requirements.txt` 기반으로 필요한 패키지를 설치합니다...\n")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    print("\n✅ 패키지 설치가 완료되었습니다.\n")

# ✅ `korail_macro.py` 실행
def run_macro():
    print("\n🚀 `korail_macro.py`를 실행합니다...\n")
    subprocess.run(["python", "korail_macro.py"])

if __name__ == "__main__":
    update_env()           # 1️⃣ 환경변수 설정
    install_requirements() # 2️⃣ 패키지 설치
    run_macro()            # 3️⃣ `korail_macro.py` 실행