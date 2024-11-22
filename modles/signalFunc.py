# import time
# import serial
#
# def validate_signal(data):
#     """
#     Validate the input signal data.
#
#     Args:
#         data (dict): The input data containing the signal.
#
#     Returns:
#         bool: True if the signal is valid, False otherwise.
#     """
#     signal = data.get('signal')
#
#     if not signal:
#         return False
#
#     # Add any additional validation here
#     # For example, you can check if the signal is in a specific format
#
#     return True
#
#
# def braille_signal(data):
#
#     signal = data.get('signal')
#
#     if signal == 'A':
#         signal = 'A'
#
#     return signal
#
# def destination(data ,arduino):
#     route = data.get('destination')
#     # 목적지에 따라 아두이노로 보낼 신호를 변수에 넣기 형식: 배열 [[방향,시간(초)]]
#     # 정지:1 전진:2 후진:3 왼쪽:4 오른쪽:5
#
#     if route == '농협':
#         route = [['2', 20], ['1', 5], ['4', 5], ['1', 5], ['5', 5], ['1', 5], ['2', 20]]
#
#
#     for i in range(len(route)):
#         arduino.write(route[i][0].encode())
#         time.sleep(route[i][1])
#
