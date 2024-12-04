# 모듈 설치
from flask import Flask, request, jsonify
import serial
import time

# import modles.signalFunc
# from modles.signalFunc import *

app = Flask(__name__)

# 아두이노 직렬 포트 설정 (라즈베리파이에 연결된 아두이노)
try:
    arduino1 = serial.Serial('/dev/ttyACM0', 9600)  # 아두이노 1(점자블록)
except serial.SerialException:
    arduino1 = serial.Serial('/dev/ttyACM1', 9600)  # 포트가 일치하지 않으면 대체 포트 사용

try:
    arduino2 = serial.Serial('/dev/ttyUSB0', 9600)  # 아두이노 2(모터)
except serial.SerialException:
    arduino2 = serial.Serial('/dev/ttyUSB1', 9600)  # 포트가 일치하지 않으면 대체 포트 사용

stop_flag = False

# 점자 출력 함수
def send_braille_signal(data):
    signal = data

    arduino1.write(signal.encode())
    print("출력:"+signal)
    time.sleep(len(signal) * 0.2)
    return signal

# 모터 이동 함수
def dirve(data):
    route = data.get('signal')
    global stop_flag
    stop_flag = False
    # 목적지에 따라 아두이노로 보낼 신호를 변수에 넣기 형식: 배열 [[방향,시간(초)]]
    # 정지:1 전진:2 후진:3 왼쪽:4 오른쪽:5
    routes = {
        '농협': [['2', 20], ['1', 5], ['4', 5], ['1', 5], ['5', 5], ['1', 5], ['2', 20]],

        '한아름실': [['2', 5], ['1', 5], ['4', 5], ['1', 5], ['2', 35], ['1', 5], ['4', 5], ['1', 5], ['2', 5], ['1', 5]],

        '위클래스': [['2', 5], ['1', 5], ['4', 5], ['1', 5], ['2', 15], ['1', 5], ['4', 5], ['1', 5], ['2', 5], ['1', 5]],

        '미술실': [['2', 5], ['1', 5], ['4', 5], ['1', 5], ['2', 25], ['1', 5], ['4', 5], ['1', 5], ['2', 5], ['1', 5]],

        '음악실': [['2', 5], ['1', 5], ['4', 5], ['1', 5], ['2', 25], ['1', 5], ['5', 5], ['1', 5], ['2', 5], ['1', 5]],

        '화장실(중앙)': [['2', 10], ['1', 5], ['4', 5], ['1', 5], ['2', 15], ['1', 5], ['5', 5], ['1', 5], ['2', 10],
                    ['1', 5]],

        '2학년 교무실': [['2', 5], ['1', 5], ['5', 5], ['1', 5], ['2', 10], ['1', 5], ['5', 5], ['1', 5], ['2', 20],
                    ['1', 5], ['5', 5], ['2', 5], ['1', 5]],

        '열린토론 학습실': [['2', 10], ['1', 5], ['4', 5], ['1', 5], ['2', 15], ['1', 5], ['5', 5], ['1', 5], ['2', 10],
                     ['1', 5], ['5', 5], ['1', 5], ['2', 10], ['4', 5], ['1', 5], ['2', 5], ['1', 5]],

        '진로활동실': [['2', 5], ['1', 5], ['5', 5], ['1', 5], ['2', 10], ['1', 5], ['5', 5], ['1', 5], ['2', 5], ['1', 5],
                  ['4', 5], ['1', 5]]
    }

    if route in routes:
        route = routes[route]
    else:
        # 목적지가 일치하지 않을 경우
        return jsonify({"message": "Invalid destination!"}), 400 # 400: Bad Request
    for i in range(len(route)):
        if stop_flag:
            send_braille_signal("정지 명령 수신")
            arduino2.write('1'.encode())
            return jsonify({"message": "정지 명령 수신"}), 200 # 200: OK
            #강제중지
        if route[i][0] == '1':
            send_braille_signal("정지")
        elif route[i][0] == '2':
            send_braille_signal("전진")
        elif route[i][0] == '3':
            send_braille_signal("후진")
        elif route[i][0] == '4':
            send_braille_signal("좌회전")
        elif route[i][0] == '5':
            send_braille_signal("우회전")
        else:
            send_braille_signal("잘못된 신호 수신, 정지합니다")
            arduino2.write('1'.encode())
            return jsonify({"message": "잘못된 신호 수신, 정지합니다"}), 500 # 500: Internal Server Error

        arduino2.write(route[i][0].encode())
        time.sleep(route[i][1])
    send_braille_signal(route+"에 도착하였습니다")

# 라즈베리파이 주소: 10.118.72.44:3000/send_signal
# 아이피 주소 확인 필수

# POST로 신호 받아 전체 작동
@app.route('/send_signal', methods=['POST'])
def send_signal():
    print(request)
    data = request.json # json 데이터 받기
    print(data)
    signal = data.get('signal') # 목적지 데이터

    # 입력 신호 검증
    if not signal:
        return jsonify({"message": "Signal not found in the request!"}), 400 # 400: Bad Request

    send_braille_signal(str(signal) + "으로 출발합니다")
    jsonify({"message": f"출발 :'{signal}' "}), 202 # 202: Accepted(확인용 메시지)
    print(signal) # 목적지 출력
    dirve(data) # 목적지로 이동
    return jsonify({"message": f"'{signal}' 작업완료"}), 200 # 200: OK


# 강제정지 (작동여부 불명(안하는거같은데))
@app.route('/stop', methods=['POST'])
def stop():
    arduino2.write('1'.encode())
    global stop_flag
    stop_flag = True
    return jsonify({"message": "정지"}), 200 # 200: OK


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)