import socket
import multiprocessing
import re
import time
# import dynamic.mini_framework
import sys


class WSGIServer:

    def __init__(self, app):
        """初始化功能，创建套接字/绑定等"""

        # 创建一个服务器套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 套接字 地址重用选项 1设置0取消
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定
        self.server_socket.bind(('', 9999))
        # 监听 被动套接字  设置已完成三次握手队列的长度
        self.server_socket.listen(128)

        self.app = app

    def request_handler(self, client_socket):
        """为每个客户进行服务"""
        recv_data = client_socket.recv(4096)
        if not recv_data:
            print("客户端已经断开连接")
            client_socket.close()
            return

        # 对接收到的数据进行解码
        request_str_data = recv_data.decode()
        # data_list = request_str_data.split("\r\n")
        # request_line = data_list[0]

        # 请求行中第一个数据 就是用户的资源请求路径
        # request_line
        # GET /index.html HTTP/1.1
        # POST /index.html HTTP/1.1
        # 通过正则表达式来提取数据，更方便
        # ret = re.match(r"[^/]+([^ ]+)", request_line)
        ret = re.match(r"[^/]+([^ ]+)", request_str_data)
        if ret:
            path_info = ret.group(1)  # /index.html
            print(">"*30, path_info)
        else:
            path_info = "/"
        print("用户请求路径是%s" % path_info)

        # 如果通过正则提取url之后，发现是/那么就意味着需要访问的是主页
        # 一般主页的名字是  /index.html
        if path_info == '/':
            path_info = '/index.html'

        # 通过if判断来区分动态请求/静态请求
        # 假如.html结尾的为动态请求
        if not path_info.endswith(".html"):
            # 如果不是以.html结尾的
            try:
                # ./html/index.html
                with open("./static/" + path_info, "rb") as f:
                    file_data = f.read()
            except Exception as e:
                # 用户请求路径是失败了
                # 响应行
                response_line = "HTTP/1.1 404 Not Found\r\n"

                # 响应头
                response_header = "Server: PythonWebServer2.0\r\n"

                # 响应体
                response_body = "ERROR!!!!!"
                # 拼接报文
                response_data = response_line + response_header + "\r\n" + response_body
                # 发送
                client_socket.send(response_data.encode())

            else:
                # 给客户端回复HTTP响应报文：响应行 + 响应头 +空行 + 响应体
                # request---->请求
                # response --->应答（响应）
                # 响应头(response_header)
                response_header = "HTTP/1.1 200 OK\r\n"
                response_header += "Server: PythonWebServer1.0\r\n"
                response_header += "\r\n"

                # 响应体(response_body)
                response_body = file_data

                # 拼接报文
                response = response_header.encode("utf-8") + response_body

                # 发送
                client_socket.send(response)
            finally:
                # 关闭套接字
                client_socket.close()
        else:
            # 如果是以.html结尾的
            # 响应头(response_header)
            """
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Server: PythonWebServer1.0\r\n"
            response_header += "Content-Type: text/html; charset=UTF-8\r\n"
            response_header += "\r\n"
            """
            env = dict()
            env['PATH_INFO'] = path_info  # /index.html

            # 响应体(response_body)
            # response_body = dynamic.mini_framework.application(env, self.set_headers)
            response_body = self.app(env, self.set_headers)
            """
            if path_info == "/index.py":
                response_body = mini_framework.index()
            elif path_info == "/center.py":
                response_body = mini_framework.center() 
            else:
                response_body = "-----not found you page-----"
            """

            # 拼接response
            response = self.response_header + response_body

            # 发送
            client_socket.send(response.encode("utf-8"))

    def set_headers(self, status, headers):
        print("-----web_server.py set_headers 被调用-----")
        # status ---> 200 OK
        # headers--->[("Content-Type", "text/html;")]
        response_header = "HTTP/1.1 %s\r\n" % status
        for temp in headers:
            response_header += "%s: %s\r\n" % (temp[0], temp[1])
        response_header += "\r\n"
        self.response_header = response_header

    def run(self):
        """等待客户端的链接，然后创建子进程为其服务"""

        while True:
            # 从队列中取出一个客户套接字用以服务
            client_socket, client_addr = self.server_socket.accept()

            p = multiprocessing.Process(target=self.request_handler, args=(client_socket,))
            p.start()
            client_socket.close()


def main():

    if len(sys.argv) != 2:
        print("请按照如下运行方式运行程序:")
        print("python3 xxxx.py mini_framework:application")
        return

    # 提取模块名以及函数名
    frame_app_name = sys.argv[1]  # mini_framework:application

    # 通过正则分别提取
    ret = re.match(r"(.*):(.*)", frame_app_name)
    if ret:
        frame_name = ret.group(1)  # mini_framework
        app_name = ret.group(2)  # application
    else:
        print("请按照如下运行方式运行程序:")
        print("python3 xxxx.py mini_framework:application")
        return

    # 添加dynamic到sys.path
    sys.path.append("./dynamic")

    # 当import frame_name的时候，python会把import后面的frame_name当做模块名，去找frame_name.py而不是把 frame_name当做变量
    # 取出其中的字符串 然后再去加载 模块的
    # import frame_name
    frame = __import__(frame_name)  # 1. 导入mini_framework 2. 让frame这变量指向刚刚被导入的模块

    # 让app这个变量指向了frame指向的模块中的指定的函数(mini_framework.applicationi)
    app = getattr(frame, app_name)  # 到frame指向的模块中找app_name指向的变量

    # 1. 创建一个server对象
    wsgi_server = WSGIServer(app)

    # 2. 调用这个对象中的运行方法
    wsgi_server.run()

if __name__ == '__main__':
    main()





































