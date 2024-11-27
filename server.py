from flask import Flask, request, jsonify
import serial
import time

# import modles.signalFunc
# from modles.signalFunc import *

app = Flask(__name__)

# 아두이노 직렬 포트 설정 (라즈베리파이에 연결된 아두이노)
arduino1 = serial.Serial('/dev/ttyACM0', 9600)  # 아두이노 1(점자블록)
arduino2 = serial.Serial('/dev/ttyUSB0', 9600)  # 아두이노 2(모터)

def send_braille_signal(data):
    signal = data

    arduino1.write(signal.encode())
    time.sleep(0.5)
    return signal

def dirve(data):
    route = data.get('signal')
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
        '2학년 교사실': [['2', 5], ['1', 5], ['5', 5], ['1', 5], ['2', 10], ['1', 5], ['5', 5], ['1', 5], ['2', 20],
                    ['1', 5], ['5', 5], ['2', 5], ['1', 5]],
        '열린토론 학습실': [['2', 10], ['1', 5], ['4', 5], ['1', 5], ['2', 15], ['1', 5], ['5', 5], ['1', 5], ['2', 10],
                     ['1', 5], ['5', 5], ['1', 5], ['2', 10], ['4', 5], ['1', 5], ['2', 5], ['1', 5]],
        '진로활동실': [['2', 5], ['1', 5], ['5', 5], ['1', 5], ['2', 10], ['1', 5], ['5', 5], ['1', 5], ['2', 5], ['1', 5],
                  ['4', 5], ['1', 5]]
    }

    if route in routes:
        route = routes[route]
    else:
        return jsonify({"message": "Invalid destination!"}), 418
    for i in range(len(route)):
        if route[i][0] == '1':
            arduino1.write("정지합니다".encode())
            time.sleep(5)
        elif route[i][0] == '2':
            arduino1.write("전진합니다".encode())
            time.sleep(5)

        elif route[i][0] == '3':
            arduino1.write("후진합니다".encode())
            time.sleep(5)

        elif route[i][0] == '4':
            arduino1.write("왼쪽으로 이동합니다".encode())
            time.sleep(5)

        elif route[i][0] == '5':
            arduino1.write("오른쪽으로 이동합니다".encode())
            time.sleep(5)

        else:
            arduino1.write(route[i][0].encode())
        arduino2.write(route[i][0].encode())
        time.sleep(route[i][1])

# 웹 서버의 POST 요청 처리
@app.route('/send_signal', methods=['POST'])
def send_signal():
    print(request)
    data = request.json
    print(data)
    signal = data.get('signal')

    # 입력 신호 검증
    if not signal:
        return jsonify({"message": "Signal not found in the request!"}), 418

    send_braille_signal(signal + "으로 출발합니다")
    print(signal)
    dirve(data)
    return jsonify({"message": f"Signal '{signal}' sent to Arduino successfully!"}), 200


    # 아두이노로 신호 보내기
    # print(f"Sending signal '{braille}' to Arduino...")
    # arduino1.write(braille.encode())  # 신호를 직렬 포트로 전송
    # time.sleep(0.5)  # 잠시 대기
    #
    # return jsonify({"message": f"Signal '{braille}' sent to Arduino successfully!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)