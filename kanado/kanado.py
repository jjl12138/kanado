# -*- coding: utf-8 -*-
# @Author : 江河
# @Email  : 2516638426@qq.com
# @Time   : 2020/4/24 14:31
# @File   : kanado
# @Project: python高级项目

import re
import time
from functools import wraps

def default(environ,start_response):
    # print('#'*100)
    # print(environ)
    # print('#'*100)
    status = '404 Not Found'
    response_headers = [('Content_Type','text/html')]
    start_response(status,response_headers)
    return  [('==404 Not Found from a simple WSGI application!--->%s\n'%time.ctime()).encode('utf-8')]

class Kanado:

    def __init__(self,import_name):
        self.import_name = import_name
        self.uri_map = {}
        self.uri_regex_map = {}
        self.uri_map = {
            '404':default
        }

    def __call__(self,*args):
        environ,start_response = args
        url = environ['PATH_INFO']

        if url in self.uri_map:
            app = self.uri_map.get(url)
            dic = {}
            return app(environ,start_response, **dic)

        for k,v in self.uri_map.items():
            if k in self.uri_regex_map:
                m = self.uri_regex_map[k].match(url)
                if m:
                    app = self.uri_map.get(k)
                    return app(environ,start_response,**m.groupdict())  # 返回的是一个字典，包含所有经命名的匹配子群，键值是子群名
        else:
            app = self.uri_map.get(url,self.uri_map['404'])
            return  app(environ,start_response)

    def route(self,path):
        print('path',path)

        pattern = path
        pattern = pattern.replace('<','(?P<')  # (?P<NAME>expr) 类似于(expr),同时给分组制定了一个别名NAME
        pattern = pattern.replace('>','>\w+)')

        def wrapper(func):

            if pattern.find('<') >= 0 and pattern.find('>') >= 0:
                self.uri_regex_map[path] = re.compile(pattern)

            @wraps(func)  # 使函数签名和文档和query_note的一致
            def _wrap(environ,start_response,*args,**param):
                res = func(*args,**param)
                start_response('200 OK',[('Content-Type','text/html')])
                return [res.encode('utf-8')]

            self.uri_map.update({
                path:_wrap,
            })
            return _wrap
        return wrapper
