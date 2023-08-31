# 接口说明
`ptz_online.py`用于接收post信息，并返回response  
详细的接口说明文档请运行```python ptz_online.py```后查看`http://127.0.0.1:8085/apidocs/`  
相关swagger接口配置保存在`demo.yml`中

# 摄像头控制
分别基于两种协议实现对摄像头的控制，onvif适用于局域网内控制，国标28181支持局域网外控制。
## 1、onvif
### prepare requirements in cmd
* onvif  
```
git clone https://github.com/FalkTannhaeuser/python-onvif-zeep.git
cd python-onvif-zeep
python setup.py install
pip3 install --upgrade onvif_zeep
```
or
```
pip install onvif-zeep
```
 报错解决  _'Onvif_hik' object has no attribute 'ptz'_
![img.png](image\img.png)
* others
```
pip install zeep time requests PIL
```
### PTZ function
get details in [ptz.wsdl](https://www.onvif.org/ver20/ptz/wsdl/ptz.wsdl "ptz.wsdl")

## 2、GB28181
### 配置说明
以TPLink摄像头为例，图中说明对应程序中的设备配置
![img_1.png](image\img_1.png)
### 任务流程
1. 程序基于国标28181，生成控制信息
2. 程序利用sip协议发送MESSAGE至摄像头![img_2.png](image\img_2.png)
3. 摄像头接收到信息，并回复200 OK信息![img_3.png](image\img_3.png)
### reference
* PTZCmd详解 https://blog.csdn.net/longlong530/article/details/9194361
* 历史代码参考 https://github.com/10961020/GB28181/blob/master/PTZ.py
* sip协议详解 https://blog.csdn.net/Chiang2018/article/details/122752294