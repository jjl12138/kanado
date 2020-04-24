# -*- coding: utf-8 -*-
# @Author : 江河
# @Email  : 2516638426@qq.com
# @Time   : 2020/4/24 20:16
# @File   : wsgi_ref
# @Project: python高级项目

# from wsgiref.simple_server import make_server,demo_app
# from app import app
#
# if __name__ == '__main__':
#     httpd = make_server(host='',port=8000,app=app)
#     print('Serving HTTP on port 8000...')
#     httpd.serve_forever()

from wsgiserver.wsgi_server import WSGIServer
# from app import app
from blog import app
import atexit

if __name__ == "__main__":
    server = WSGIServer("127.0.0.1",8889,app)
    atexit.register(server.server_close)
    print('running http://{}:{}'.format("127.0.0.1",8889))
    server.serve_forever()
