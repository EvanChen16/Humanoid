# import serial

# ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

# while True:
#     received_lines = ser.readlines()
    
#     if received_lines:
#         for line in received_lines:
#             hex_values = ' '.join([format(byte, '02X') for byte in line])
#             print("Hex values:", hex_values)



import serial
import struct
import time

# 初始化串口（根据你的配置）
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

# 模拟函数中的变量和封包
Desire_Set = True
IMU_Reset = False
ForceState = False
Gain_Set = False

SENSOR_SET_PACKAGE_SIZE = 12
sensorsetpackage = bytearray(SENSOR_SET_PACKAGE_SIZE)
while True:
    sensorsetpackage[0] = 0x53
    sensorsetpackage[1] = 0x54
    sensorsetpackage[2] = 0xF6

    Desire_Roll = 0  # 你需要设定 Desire_Roll 的实际值
    Desire_Pitch = 0  # 你需要设定 Desire_Pitch 的实际值
    Desire_Yaw = 0  # 你需要设定 Desire_Yaw 的实际值

    if Desire_Roll < 0:
        Desire_Roll = ~(Desire_Roll) + 1
        sensorsetpackage[3] = ((Desire_Roll >> 8) & 0xFF) | 0x80
        sensorsetpackage[4] = Desire_Roll & 0xFF
        Desire_Roll = ~(Desire_Roll - 1)
    else:
        sensorsetpackage[3] = (Desire_Roll >> 8) & 0xFF
        sensorsetpackage[4] = Desire_Roll & 0xFF

    if Desire_Pitch < 0:
        Desire_Pitch = ~(Desire_Pitch) + 1
        sensorsetpackage[5] = ((Desire_Pitch >> 8) & 0xFF) | 0x80
        sensorsetpackage[6] = Desire_Pitch & 0xFF
        Desire_Pitch = ~(Desire_Pitch - 1)
    else:
        sensorsetpackage[5] = (Desire_Pitch >> 8) & 0xFF
        sensorsetpackage[6] = Desire_Pitch & 0xFF

    if Desire_Yaw < 0:
        Desire_Yaw = ~(Desire_Yaw) + 1
        sensorsetpackage[7] = ((Desire_Yaw >> 8) & 0xFF) | 0x80
        sensorsetpackage[8] = Desire_Yaw & 0xFF
        Desire_Yaw = ~(Desire_Yaw - 1)
    else:
        sensorsetpackage[7] = (Desire_Yaw >> 8) & 0xFF
        sensorsetpackage[8] = Desire_Yaw & 0xFF

    sensorsetpackage[9] = (Gain_Set << 3) | (ForceState << 2) | (IMU_Reset << 1) | Desire_Set

    sensorsetpackage[10] = 0

    sensorsetpackage[11] = 0x45
    hex_string = ' '.join([format(byte, '02X') for byte in sensorsetpackage])

    print(hex_string)
    # 将数据以十六进制形式发送到串口
    # ser.write(hex_string)
    ser.write(bytearray.fromhex(hex_string.replace(' ', '')))

    # print("send success")

    # 延时一段时间
    time.sleep(0.1)

    # 读取串口数据
    received_lines = ser.readlines()
    
    if received_lines:
        for line in received_lines:
            for byte in line:
                hex_values = format(byte, '02X')
                print("Hex value:", hex_values)
                time.sleep(0.1)

# 关闭串口连接
# ser.close()
