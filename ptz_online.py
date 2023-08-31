from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from hk_ptz_GB28181 import send_ptz_message

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
            result = {"code": "500", "msg": f"error:{msg}"}
    else:
        result = {"code": "500", "msg": "It's not a POST operation!"}
    return jsonify(result)


if __name__ == "__main__":
    server.run(port=8085, debug=True)
