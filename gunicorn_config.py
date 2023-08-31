# gunicorn_config.py
# gunicorn守护配置文件

# 绑定的主机和端口
bind = "0.0.0.0:8000"

# 工作进程数
workers = 4

# 每个工作进程处理的最大请求数
max_requests = 1000

# 每个工作进程退出后立即重启
preload_app = True

# 日志文件路径
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
