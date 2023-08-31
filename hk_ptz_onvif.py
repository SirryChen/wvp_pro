from onvif import ONVIFCamera
import zeep
import time
import requests
from requests.auth import HTTPDigestAuth
from PIL import Image


def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue


class Onvif_hik(object):
    def __init__(self, ip: str, username: str, password: str):
        self.ip = ip
        self.username = username
        self.password = password
        zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue
        self.save_path = "./{}T{}.jpg".format(self.ip, str(time.time()))  # 截图保存路径

    def content_cam(self):
        """
        链接相机地址
        :return:
        """
        self.mycam = ONVIFCamera(self.ip, 80, self.username, self.password)
        self.media = self.mycam.create_media_service()  # 创建媒体服务
        self.media_profile = self.media.GetProfiles()[0]  # 获取配置信息
        self.ptz = self.mycam.create_ptz_service()  # 创建控制台服务
        # try:
        #     self.mycam = ONVIFCamera(self.ip, 80, self.username, self.password)
        #     self.media = self.mycam.create_media_service()  # 创建媒体服务
        #     self.media_profile = self.media.GetProfiles()[0]  # 获取配置信息
        #     self.ptz = self.mycam.create_ptz_service()  # 创建控制台服务
        #     return True
        # except Exception as e:
        #     print(e)
        #     print("未连接摄像头")
        #     return False

    def Snapshot(self, picname):
        """
        截图
        :return:
        """
        res = self.media.GetSnapshotUri({'ProfileToken': self.media_profile.token})
        response = requests.get(res.Uri, auth=HTTPDigestAuth(self.username, self.password))
        with open(picname + '.jpg', 'wb') as f:  # 保存截图
            f.write(response.content)

    def Snapshot_newsize(self, picname, new_size=None):
        """
        截图并调整尺寸
        :param picname: 保存截图的文件名
        :param new_size: 调整后的尺寸，格式为(width, height)
        """
        res = self.media.GetSnapshotUri({'ProfileToken': self.media_profile.token})
        response = requests.get(res.Uri, auth=HTTPDigestAuth(self.username, self.password))
        with open(picname, 'wb') as f:
            f.write(response.content)
        if new_size:
            with Image.open(picname) as img:
                img = img.resize(new_size)
                img.save(picname)

    def get_presets(self):
        """
        获取预置点列表
        :return:预置点列表--所有的预置点
        """
        presets = self.ptz.GetPresets({'ProfileToken': self.media_profile.token})  # 获取所有预置点,返回值：list
        return presets

    def goto_preset(self, presets_token: int):
        """
        移动到指定预置点
        :param presets_token: 目的位置的token，获取预置点返回值中
        :return:
        """
        try:
            self.ptz.GotoPreset(
                {'ProfileToken': self.media_profile.token, "PresetToken": presets_token})  # 移动到指定预置点位置
        except Exception as e:
            print(e)

    def zoom(self, zoom: str, timeout: int = 0.1):
        """
        变焦
        :param zoom: 拉近或远离
        :param timeout: 生效时间
        :return:
        """
        request = self.ptz.create_type('ContinuousMove')
        request.ProfileToken = self.media_profile.token
        request.Velocity = {"Zoom": zoom}
        self.ptz.ContinuousMove(request)
        time.sleep(timeout)
        self.ptz.Stop({'ProfileToken': request.ProfileToken})

    def relative_move(self, pan: float = 0.1, tilt: float = 0.1):
        """
        相对运动
        :param pan: 相对水平角度，-1~1
        :param tilt: 相对垂直角度，-1~1
        :return:
        """
        try:
            self.ptz.RelativeMove(
                {'ProfileToken': self.media_profile.token, "Translation": {'PanTilt': {'x': pan, 'y': tilt}}})  # 移动到指定预置点位置
        except Exception as e:
            print(e)


if __name__ == '__main__':
    monitor_address = "http://192.168.10.20:5060/onvif/service"    # FIXME
    user_name = "admin"
    Password = "a12345678"

    aa = Onvif_hik(monitor_address, user_name, Password)  # 初始化类
    aa.content_cam()
    presets = aa.get_presets()
    print("预置点：{}".format(presets))

# test
    # 移动到预置点
    # aa.goto_preset(1)
    # time.sleep(10)
    # aa.goto_preset(50)
    # time.sleep(10)
    # aa.goto_preset(100)
    # time.sleep(10)

    # 相对运动
    # aa.relative_move()
    time.sleep(5)
    aa.relative_move(-0.1, 0.0)

