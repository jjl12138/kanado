# -*- coding: utf-8 -*-
# @Author : 江河
# @Email  : 2516638426@qq.com
# @Time   : 2020/4/22 7:29
# @File   : statichttpserver
# @Project: python高级项目

import selectors
import socket
import time

from wsgiserver.http_parsed import BaseRequest

_weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_monthname = [None,  # Dummy so we can use 1-based month numbers
              "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def format_date_time(timestamp):
    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
    return "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (_weekdayname[wd], day, _monthname[month], year, hh, mm, ss)

class WSGIServer(object):

    def __init__(self,host,port,application):
        self.app = application
        self.selector = selectors.DefaultSelector()
        self.sock = socket.socket()
        self.address = (host,port)
        self.request_queue_size = 5
        self.open_socket()



    def accept(self,sock,mask):
        sel = self.selector
        conn,addr = sock.accept()  # Should be ready      conn是socket对象
        conn.setblocking(False)
        sel.register(conn,selectors.EVENT_READ,self.read)


    def write(self,sock,mask):

        print('write')
        sel = self.selector

        # # 组织相应的头信息(header)
        # response_headers = "HTTP/1.1 200 OK\r\n"  # 200表示找到这个资源
        # response_headers += "\r\n"  # 用一个空的行与body进行隔开
        # # 组织 内容(body)
        # response_body = "Hello World"
        #
        # response = response = response_headers + response_body
        # sock.send(response.encode("utf-8"))
        body = self.app(self.req.getenv(), self.start_response)

        for data in body:
            self.response += data

        resp = self.response
        sock.send(resp)

        sel.unregister(sock)
        sock.close()

    def read(self,conn,mask):
        sel = self.selector

        data = conn.recv(1000)  # should be ready
        if data:
            conn.setblocking(False)
            sel.unregister(conn)

            # print('echoing',repr(data))

            s = data.decode('utf-8')
            self.req = BaseRequest(s)
            # print(self.req.headers)
            # print(self.req.url)
            # print(self.req.method)

            sel.register(conn,selectors.EVENT_WRITE,self.write)
        else:
            print('closing',conn)
            sel.unregister(conn)
            conn.close()


    def server_close(self):
        self.sock.close()
        self.selector.close()


    def server_bind(self):
        """
        绑定
        :return:
        """
        sock = self.sock

        sock.bind(self.address)
        self.server_address = sock.getsockname()


    def server_listen(self):
        """
        监听
        :return:
        """
        self.sock.listen(self.request_queue_size)


    def open_socket(self):
        sock = self.sock

        self.server_bind()
        self.server_listen()
        sock.setblocking(False)


    def serve_forever(self):
        sock = self.sock  # 套接字
        sel = self.selector  # 默认选择器 selectors.DefaultSelector()

        sel.register(sock,selectors.EVENT_READ,self.accept)  # 第三个参数就是key.data
        try:
            while True:
                events = sel.select()  # sel.select() 为非阻塞
                for key,mask in events:  # key.fileobject：哪个socket触发了事件，mask：哪个事件被触发
                    callback = key.data
                    callback(key.fileobj,mask)

        finally:
            print('close')
            self.server_close()

    def start_response(self,status,headers_list):
        """

        :param status:
        :param headers_list:
        :return:
        """

        r = 'HTTP/1.1 {}\r\n'.format(status)
        for h in headers_list:
            k = h[0]
            v = h[1]
            r += '{}:{}\r\n'.format(k,v)

        r += "Date: %s\r\n" % format_date_time(time.time())
        r += "Server:neuedu-wsgi\r\n"
        r +='\r\n'

        self.response = r.encode()




if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8889
    print('running http://{}:{}'.format(host,port))
    httpd = WSGIServer(host,port)
    httpd.serve_forever()
