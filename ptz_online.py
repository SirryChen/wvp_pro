from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from hk_ptz_GB28181 import send_ptz_message
from gunicorn.app.base import BaseApplication
import socket

server = Flask(__name__)
Swagger(server)
server.config['JSON_AS_ASCII'] = False


@server.route('/flask/flasgger/demo', methods=['POST'])
@swag_from('demo.yml')
def demo_request():
    if request.method == "POST":
        args_json = request.json
        # print(args_json)
        # args_str = json.loads(args_json)
        args_str = args_json
        hk_camera_ip = args_str.get("hk_camera_ip")
        hk_camera_id = args_str.get("hk_camera_id")
        hk_camera_port = args_str.get("hk_camera_port", 5060)
        ptz_cmd = args_str.get("ptz_cmd")
        ptz_speed = args_str.get("ptz_speed", 31)
        msg = send_ptz_message(hk_camera_ip, hk_camera_id, hk_camera_port, ptz_cmd, ptz_speed)
        if msg == "success":
            result = {"code": "200", "msg": "SUCCESS"}
        else:
            result = {"code": "400", "msg": f"error:{msg}"}
    else:
        result = {"code": "500", "msg": "It's not a POST operation!"}
    return jsonify(result)


if __name__ == "__main__":
    # server.run(port=8085, debug=True)     # for debug


    class GunicornApp(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application


    my_device_ip = socket.gethostbyname(socket.gethostname())
    gunicorn_options = {
        'bind': f'{my_device_ip}:{8085}',
        'workers': 4  # 适当调整 worker 数量
    }
    GunicornApp(server, gunicorn_options).run()
