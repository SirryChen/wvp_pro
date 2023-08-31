## 接口文档
### URL
`http://[ip]:[port]/flask/flasgger/demo`

### 参数说明
| 参数             |类型| 允许值                                                         |
|----------------|-----|-------------------------------------------------------------|
| hk_camera_ip   |string||
| hk_camera_id   |string||
| hk_camera_port |string||
| ptz_cmd        |string| 'LEFT', 'RIGHT', 'DOWN', 'UP', 'ZOOM_IN', 'ZOOM_OUT', 'STOP' |
| ptz_speed      |int| [0,255]                                                     |

### 响应说明
#### 响应成功
```json
{
  "code": "200",
  "msg": "SUCCESS"
}
```
#### 响应失败
- 程序错误
```json
{
  "code": "400",
  "msg": "error:"
}
```
- 发送类型错误
```json
{
  "code": "500", 
  "msg": "It's not a POST operation!"
}
```
