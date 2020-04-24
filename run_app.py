# -*- coding: utf-8 -*-
# @Author : 江河
# @Email  : 2516638426@qq.com
# @Time   : 2020/4/24 11:39
# @File   : run_app.py
# @Project: python高级项目

from wsgiserver.wsgi_server import WSGIServer
from app import app
# from blog import app as application
import atexit

if __name__ == "__main__":
    server = WSGIServer("127.0.0.1",8889,app)  # application = app,即flask框架
    atexit.register(server.server_close)  # atexit模块主要的作用就是在程序即将结束之前执行的代码，atexit模块使用register函数用于注册程序退出时的回调函数，然后在回调函数中做一些资源清理的操作
    print("running http://{}:{}".format("127.0.0.1",8889))
    server.serve_forever()

