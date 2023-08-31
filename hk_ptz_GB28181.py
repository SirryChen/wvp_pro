import socket
import random
import string
import time


def generate_random_string(length):
    # 从大小写字母和数字中随机选择
    letters_and_digits = string.ascii_letters + string.digits
    # 生成指定长度的随机字符串
    return ''.join(random.choices(letters_and_digits, k=length))


def ptz_cmd_encode(ptz_cmd, ptz_speed):
    """
    按照国标28181生成控制码
    :param ptz_cmd:
    :param ptz_speed:
    :return:
    """
    ptz_string = ['LEFT', 'RIGHT', 'DOWN', 'UP', 'ZOOM_IN', 'ZOOM_OUT', 'STOP']
    assert ptz_cmd in ptz_string, "控制命令错误"

    ptz_codes = [0x02, 0x01, 0x04, 0x08, 0x10, 0x20, 0x00]
    ptz_code = ptz_codes[ptz_string.index(ptz_cmd)]  # 指令码
    left_right_speed = int((ptz_code & 0b000011) != 0) * ptz_speed
    up_down_speed = int((ptz_code & 0b001100) != 0) * ptz_speed
    zoom_speed = int((ptz_code & 0b110000) != 0) * ptz_speed
    check_code = hex((0xa5 + 0x0f + 0x01 + ptz_code + left_right_speed + up_down_speed + zoom_speed) % 0x100)[2:]
    converted_ptz_cmd = "a50f01{:0>2}{:0>2}{:0>2}{:0>2}{:0>2}".format(ptz_code, hex(left_right_speed)[2:],
                                                                      hex(up_down_speed)[2:],
                                                                      hex(zoom_speed)[2:], check_code)

    return converted_ptz_cmd


def send_ptz_message(camera_ip, camera_id, camera_port, ptz_cmd, ptz_speed=200, device_id=18062804121310234425):
    """
    基于国标28181，通过sip协议向摄像头终端发送控制信息
    :param camera_ip: 摄像头接入的ip地址
    :param camera_id: 摄像头内部设置的唯一标识id
    :param camera_port: 摄像头内部设置的接入端口
    :param ptz_cmd: 控制命令，包括：'left', 'right', 'down', 'up', 'zoom in', 'zoom out', 'stop'
    :param ptz_speed: 摄像头执行控制命令的速度
    :param device_id: 自定义的设备sip url唯一标识
    """
    try:
        converted_ptz_cmd = ptz_cmd_encode(ptz_cmd, ptz_speed)
        my_device_ip = socket.gethostbyname(socket.gethostname())
        print(my_device_ip)
        ptz_message = "<?xml version=\"1.0\"?>\r\n" \
                      "<Control>\r\n" \
                      "<CmdType>DeviceControl</CmdType>\r\n" \
                      "<SN>11</SN>\r\n" \
                      f"<DeviceID>{camera_id}</DeviceID>\r\n" \
                      f"<PTZCmd>{converted_ptz_cmd}</PTZCmd>\r\n" \
                      "<Info>\r\n" \
                      "<ControlPriority>5</ControlPriority>\r\n" \
                      "</Info>\r\n" \
                      "</Control>"
        sip_message = f"MESSAGE sip:{camera_id}@{camera_ip}:{camera_port} SIP/2.0\r\n" \
                      f"Via: SIP/2.0/UDP {my_device_ip}:1024;rport;branch={generate_random_string(10)}\r\n" \
                      f"From: <sip:{device_id}@{my_device_ip}:1024>;tag={generate_random_string(6)}\r\n" \
                      f"To: <sip:{camera_id}@{camera_ip}:{camera_port}>\r\n" \
                      f"Call-ID: {generate_random_string(10)}\r\n" \
                      "CSeq: 20 MESSAGE\r\n" \
                      "Max-Forwards: 70\r\n" \
                      "Content-Type: Application/MANSCDP+xml\r\n" \
                      f"Content-Length: {len(ptz_message)}\r\n" \
                      "Require: response\r\n\r\n"
        message = sip_message + ptz_message
        print(message)
        # 创建UDP套接字并发送SIP消息
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.bind(("192.168.10.103", 5060))
        sock.bind((my_device_ip, 5060))
        sock.sendto(message.encode(), (camera_ip, camera_port))

        print("发送完成")
        return 'success'
    except Exception as e:
        return e


if __name__ == "__main__":
    # 摄像机SIP地址和端口号
    hk_camera_ip = "192.168.10.20"
    hk_camera_id = "34020000001320000020"
    hk_camera_port = 5056

    # send_ptz_message(hk_camera_ip, hk_camera_id, hk_camera_port, ptz_cmd="down")
    # time.sleep(5)
    send_ptz_message(hk_camera_ip, hk_camera_id, hk_camera_port, ptz_cmd="down")
